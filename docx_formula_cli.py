#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量修正Markdown文件中的LaTeX公式格式问题 - 增强版
用法: python fix_latex_formulas.py input.md [output.md]
      python fix_latex_formulas.py -d input_directory [-o output_directory] [-r]
"""

import sys
import os
import re
import argparse

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
    modified_count = 0
    
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
            modified_count += 1
    
    return processed_content, modified_count

def process_directory(input_dir, output_dir=None, recursive=False):
    """
    处理整个目录下的Markdown文件
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录，默认在原目录创建processed_markdown子目录
        recursive: 是否递归处理子目录
    """
    if output_dir is None:
        output_dir = os.path.join(input_dir, "processed_markdown")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 获取所有markdown文件
    files_to_process = []
    if recursive:
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.md'):
                    rel_dir = os.path.relpath(root, input_dir)
                    files_to_process.append((os.path.join(root, file), 
                                            os.path.join(output_dir, rel_dir)))
    else:
        for file in os.listdir(input_dir):
            if file.endswith('.md'):
                files_to_process.append((os.path.join(input_dir, file), output_dir))
    
    # 处理每个文件
    success_count = 0
    total_formulas_modified = 0
    
    print(f"找到 {len(files_to_process)} 个Markdown文件需要处理")
    
    for file_path, out_dir in files_to_process:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        file_name = os.path.basename(file_path)
        output_file = os.path.join(out_dir, file_name)
        
        print(f"处理文件: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 预处理LaTeX公式
            processed_content, modified_count = preprocess_latex_formulas(content)
            total_formulas_modified += modified_count
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(processed_content)
                
            success_count += 1
            print(f"  完成: {output_file} (修正了 {modified_count} 个公式)")
        except Exception as e:
            print(f"  处理失败: {e}")
    
    print(f"批量处理完成: {success_count}/{len(files_to_process)} 个文件成功")
    print(f"共修正了 {total_formulas_modified} 个公式格式问题")
    
    return success_count == len(files_to_process)

def process_file(input_file, output_file=None):
    """
    处理单个Markdown文件
    
    Args:
        input_file: 输入文件
        output_file: 输出文件，默认为在原文件名前加"fixed_"
    """
    if output_file is None:
        base_dir = os.path.dirname(input_file)
        base_name = os.path.basename(input_file)
        output_file = os.path.join(base_dir, f"fixed_{base_name}")
    
    print(f"处理文件: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 预处理LaTeX公式
        processed_content, modified_count = preprocess_latex_formulas(content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)
            
        print(f"处理完成: {output_file}")
        print(f"共修正了 {modified_count} 个公式格式问题")
        return True
    except Exception as e:
        print(f"处理失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='修正Markdown文件中的LaTeX公式格式问题')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('input', nargs='?', help='输入文件')
    group.add_argument('-d', '--directory', help='输入目录')
    
    parser.add_argument('-o', '--output', help='输出文件或目录')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归处理子目录')
    
    args = parser.parse_args()
    
    if args.directory:
        # 目录处理模式
        if not os.path.isdir(args.directory):
            print(f"错误: 目录不存在 - {args.directory}")
            return False
            
        return process_directory(args.directory, args.output, args.recursive)
    else:
        # 单文件处理模式
        if not os.path.exists(args.input):
            print(f"错误: 文件不存在 - {args.input}")
            return False
            
        return process_file(args.input, args.output)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)