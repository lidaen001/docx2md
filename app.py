import os
import tempfile
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import io
import docx
from docx.document import Document as DocxDocument
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
from pix2text import Pix2Text
import re
import base64
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB限制

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 初始化pix2text
p2t = Pix2Text.from_config(enable_formula=True)

def preprocess_latex_formulas(markdown_content):
    """
    全面预处理Markdown中的LaTeX公式，修复各种格式问题
    
    Args:
        markdown_content: 原始Markdown内容
        
    Returns:
        处理后的Markdown内容
    """
    import re
    
    # 查找所有LaTeX公式块
    formula_pattern = r'(\$\$.*?\$\$)'
    formulas = re.findall(formula_pattern, markdown_content, re.DOTALL)
    
    # 如果没有找到公式，直接返回原内容
    if not formulas:
        return markdown_content
    
    processed_content = markdown_content
    
    for formula in formulas:
        original_formula = formula
        processed_formula = formula
        
        # 1. 处理带有多余空格的文本标识符
        # 标识一系列可能需要处理的文本标识符模式
        text_identifiers = [
            # 基本数学符号和函数名
            (r'([A-Za-z])\s+([A-Za-z])', r'\1\2'),  # 移除字母间的空格
            (r'([A-Za-z]+)\s*_\s*([A-Za-z0-9]+)', r'\1_\2'),  # 修复下标间的空格
            (r'([A-Za-z]+)\s*\^\s*([A-Za-z0-9]+)', r'\1^\2'),  # 修复上标间的空格
            
            # 特定函数名和操作符
            (r't\s*a\s*n\s*h', r'tanh'),
            (r'o\s*p\s*e\s*r\s*a\s*t\s*o\s*r', r'operator'),
            (r'f\s*r\s*a\s*c', r'frac'),
            (r'l\s*e\s*f\s*t', r'left'),
            (r'r\s*i\s*g\s*h\s*t', r'right'),
            (r's\s*u\s*m', r'sum'),
            (r'p\s*r\s*o\s*d', r'prod'),
            (r'l\s*i\s*m', r'lim'),
            (r'i\s*n\s*t', r'int'),
            
            # 常见数学符号和结构
            (r'\\s*i\s*n', r'\\in'),
            (r'\\s*subset', r'\\subset'),
            (r'\\s*cup', r'\\cup'),
            (r'\\s*cap', r'\\cap'),
            (r'\\s*mathbb', r'\\mathbb'),
            (r'\\s*mathrm', r'\\mathrm'),
            (r'\\s*mathcal', r'\\mathcal'),
            
            # 常见的空格文本标识符(从实例中提取)
            (r'S\s+h\s+i\s+p', r'Ship'),
            (r'F\s+a\s+u\s+l\s+t', r'Fault'),
            (r'E\s+v\s+a\s+l\s+u\s+a\s+t\s+e', r'Evaluate'),
            (r'I\s+n\s+d\s+e\s+x', r'Index'),
            (r'B\s+u\s+g', r'Bug'),
            (r'T\s+r\s+e\s+n\s+d', r'Trend'),
            (r'S\s+i\s+m', r'Sim')
        ]
        
        # 应用所有文本替换模式
        for pattern, replacement in text_identifiers:
            processed_formula = re.sub(pattern, replacement, processed_formula)
        
        # 2. 修复其他常见的格式问题
        # 处理LaTeX命令的格式问题
        processed_formula = re.sub(r'\\operatorname\s*{\s*([^}]+)\s*}', r'\\operatorname{\1}', processed_formula)
        processed_formula = re.sub(r'\\text\s*{\s*([^}]+)\s*}', r'\\text{\1}', processed_formula)
        
        # 处理括号和特殊符号的格式问题
        processed_formula = re.sub(r'~\s+', r'~ ', processed_formula)  # 统一波浪号后的空格
        processed_formula = re.sub(r',\s+', r', ', processed_formula)  # 统一逗号后的空格
        
        # 处理下标和上标的格式问题
        processed_formula = re.sub(r'_\s*{\s*([^}]+)\s*}', r'_{\1}', processed_formula)
        processed_formula = re.sub(r'\^\s*{\s*([^}]+)\s*}', r'^{\1}', processed_formula)
        
        # 修复多余的空格
        processed_formula = re.sub(r'\\\s+', r'\\', processed_formula)  # 反斜杠后的空格
        processed_formula = re.sub(r'\s+\\', r'\\', processed_formula)  # 反斜杠前的空格
        processed_formula = re.sub(r'\s+{', r'{', processed_formula)    # 左花括号前的空格
        processed_formula = re.sub(r'}\s+', r'}', processed_formula)    # 右花括号后的空格
        
        # 处理分数的格式问题
        processed_formula = re.sub(r'\\frac\s*{\s*([^}]+)\s*}\s*{\s*([^}]+)\s*}', r'\\frac{\1}{\2}', processed_formula)
        
        # 只有当公式有变化时才替换
        if processed_formula != original_formula:
            processed_content = processed_content.replace(original_formula, processed_formula)
    
    return processed_content

def preprocess_single_formula(latex):
    """预处理单个LaTeX公式字符串"""
    import re
    
    # 应用与完整预处理相同的规则集
    text_identifiers = [
        # 基本数学符号和函数名
        (r'([A-Za-z])\s+([A-Za-z])', r'\1\2'),  # 移除字母间的空格
        (r'([A-Za-z]+)\s*_\s*([A-Za-z0-9]+)', r'\1_\2'),  # 修复下标间的空格
        (r'([A-Za-z]+)\s*\^\s*([A-Za-z0-9]+)', r'\1^\2'),  # 修复上标间的空格
        
        # 特定函数名和操作符
        (r't\s*a\s*n\s*h', r'tanh'),
        (r'o\s*p\s*e\s*r\s*a\s*t\s*o\s*r', r'operator'),
        (r'f\s*r\s*a\s*c', r'frac'),
        (r'l\s*e\s*f\s*t', r'left'),
        (r'r\s*i\s*g\s*h\s*t', r'right'),
        (r's\s*u\s*m', r'sum'),
        
        # 常见的空格文本标识符
        (r'S\s+h\s+i\s+p', r'Ship'),
        (r'F\s+a\s+u\s+l\s+t', r'Fault'),
        (r'E\s+v\s+a\s+l\s+u\s+a\s+t\s+e', r'Evaluate'),
        (r'I\s+n\s+d\s+e\s+x', r'Index'),
        (r'B\s+u\s+g', r'Bug'),
        (r'T\s+r\s+e\s+n\s+d', r'Trend'),
        (r'S\s+i\s+m', r'Sim')
    ]
    
    for pattern, replacement in text_identifiers:
        latex = re.sub(pattern, replacement, latex)
    
    # 处理其他格式问题同上
    latex = re.sub(r'\\operatorname\s*{\s*([^}]+)\s*}', r'\\operatorname{\1}', latex)
    latex = re.sub(r'~\s+', r'~ ', latex)
    latex = re.sub(r',\s+', r', ', latex)
    latex = re.sub(r'_\s*{\s*([^}]+)\s*}', r'_{\1}', latex)
    latex = re.sub(r'\^\s*{\s*([^}]+)\s*}', r'^{\1}', latex)
    
    return latex

def get_document_elements(document):
    """
    提取文档中所有元素（段落和表格）的顺序列表
    """
    elements = []
    parent_elements = document.element.body
    for child in parent_elements.iterchildren():
        if isinstance(child, CT_P):
            elements.append(Paragraph(child, document))
        elif isinstance(child, CT_Tbl):
            elements.append(Table(child, document))
    return elements

def extract_runs_with_images(paragraph):
    """
    从段落中提取所有包含图片的runs和它们的位置
    返回: [(run索引, run对象), ...]
    """
    image_runs = []
    for i, run in enumerate(paragraph.runs):
        if run.element.findall('.//w:drawing', namespaces=docx.oxml.ns.nsmap):
            image_runs.append((i, run))
    return image_runs

def extract_formula_from_image(image):
    """
    从图像中提取公式并预处理
    """
    try:
        latex = p2t.recognize_formula(image)
        # 预处理单个公式
        latex = preprocess_single_formula(latex)
        return latex
    except Exception as e:
        print(f"识别公式失败: {e}")
        return "*[公式识别失败]*"

def process_docx_with_accurate_positioning(docx_path):
    """
    处理docx文件，保持原始内容的精确顺序
    """
    doc = docx.Document(docx_path)
    
    # 获取完整的文档元素顺序
    doc_elements = get_document_elements(doc)
    
    # 提取所有图片和它们的确切位置
    images_data = []  # [(element_index, run_index, image_object), ...]
    
    print("正在从文档中提取图片...")
    for elem_idx, element in enumerate(doc_elements):
        if isinstance(element, Paragraph):
            # 处理段落中的图片
            image_runs = extract_runs_with_images(element)
            for run_idx, run in image_runs:
                # 从run中提取所有图片
                for inline in run.element.findall('.//wp:inline', namespaces=docx.oxml.ns.nsmap):
                    blip = inline.find('.//a:blip', namespaces=docx.oxml.ns.nsmap)
                    if blip is not None:
                        rId = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        if rId:
                            try:
                                image_data = doc.part.related_parts[rId].blob
                                image = Image.open(io.BytesIO(image_data))
                                # 存储图片对象和位置信息
                                images_data.append((elem_idx, run_idx, image))
                                print(f"  发现图片: 元素 #{elem_idx}, Run #{run_idx}")
                            except Exception as e:
                                print(f"  提取图片时出错: {e}")
    
    print(f"共发现 {len(images_data)} 个图片")
    
    # 生成Markdown文本，精确保持原始顺序
    markdown_content = ""
    
    # 用于跟踪当前处理的图片索引
    image_index = 0
    
    print("正在处理文档内容和识别公式...")
    # 处理每个文档元素
    for elem_idx, element in enumerate(doc_elements):
        if isinstance(element, Paragraph):
            # 创建段落的markdown内容
            para_text = ""
            
            # 获取段落中所有包含图片的runs
            image_runs = extract_runs_with_images(element)
            image_run_indices = [idx for idx, _ in image_runs]
            
            # 处理段落中的每个run
            for run_idx, run in enumerate(element.runs):
                if run_idx in image_run_indices:
                    # 这个run包含图片，找到并处理当前位置的所有图片
                    while (image_index < len(images_data) and 
                           images_data[image_index][0] == elem_idx and 
                           images_data[image_index][1] == run_idx):
                        
                        formula_image = images_data[image_index][2]
                        
                        # 使用pix2text识别公式并进行预处理
                        print(f"  正在识别公式: 元素 #{elem_idx}, Run #{run_idx}")
                        latex = extract_formula_from_image(formula_image)
                        print(f"  识别结果: {latex[:30]}..." if len(latex) > 30 else f"  识别结果: {latex}")
                        
                        # 添加识别出的公式
                        para_text += f"$$\n{latex}\n$$"
                        
                        # 移动到下一个图片
                        image_index += 1
                
                # 添加run中的文本内容
                if run.text:
                    para_text += run.text
            
            # 根据段落样式设置标题格式
            if hasattr(element, 'style') and element.style and element.style.name.startswith('Heading'):
                try:
                    level = int(element.style.name.replace('Heading', ''))
                    markdown_content += '#' * level + ' ' + para_text + "\n\n"
                except ValueError:
                    # 默认使用H2
                    markdown_content += '## ' + para_text + "\n\n"
            else:
                # 普通段落
                markdown_content += para_text + "\n\n"
        
        elif isinstance(element, Table):
            # 简单处理表格(可以根据需要扩展)
            print(f"  发现表格: 元素 #{elem_idx} (只做简单处理)")
            markdown_content += "*[表格内容]*\n\n"
    
    print("处理完成，正在进行公式格式预处理...")
    # 最后对整个内容再次预处理，确保所有公式格式正确
    markdown_content = preprocess_latex_formulas(markdown_content)
    
    return markdown_content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('没有选择文件')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('没有选择文件')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 生成唯一的处理ID
        process_id = str(uuid.uuid4())
        
        # 处理文档
        try:
            print(f"开始处理文件: {filename}")
            markdown_content = process_docx_with_accurate_positioning(file_path)
            
            # 保存处理后的markdown文件
            markdown_filename = f"{os.path.splitext(filename)[0]}.md"
            markdown_path = os.path.join(app.config['UPLOAD_FOLDER'], markdown_filename)
            
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"文件处理完成，已保存为: {markdown_filename}")
            # 重定向到预览页面
            return redirect(url_for('preview_markdown', filename=filename, md_filename=markdown_filename))
        
        except Exception as e:
            flash(f'处理文件时出错: {str(e)}')
            return redirect(url_for('index'))
    
    flash('不支持的文件类型')
    return redirect(url_for('index'))

@app.route('/preview/<filename>')
def preview_markdown(filename):
    """预览转换后的Markdown文件"""
    md_filename = request.args.get('md_filename', '')
    if not md_filename:
        md_filename = f"{os.path.splitext(filename)[0]}.md"
    
    markdown_path = os.path.join(app.config['UPLOAD_FOLDER'], md_filename)
    
    # 读取markdown内容
    try:
        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # 预处理LaTeX公式 (以防之前没有处理完全)
        markdown_content = preprocess_latex_formulas(markdown_content)
        
        # 更新文件内容为预处理后的版本
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
    except Exception as e:
        flash(f'读取Markdown文件时出错: {str(e)}')
        return redirect(url_for('index'))
    
    return render_template('preview.html', 
                          filename=filename, 
                          md_filename=md_filename, 
                          markdown_content=markdown_content)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
        as_attachment=True,
        download_name=filename
    )

@app.route('/update_markdown', methods=['POST'])
def update_markdown():
    """更新Markdown内容"""
    md_filename = request.form.get('md_filename')
    content = request.form.get('content')
    
    if not md_filename or not content:
        return jsonify({'success': False, 'message': '参数错误'}), 400
    
    try:
        # 预处理LaTeX公式
        content = preprocess_latex_formulas(content)
        
        markdown_path = os.path.join(app.config['UPLOAD_FOLDER'], md_filename)
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)