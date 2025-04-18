1.一种船舶机电装备虚拟环境中故障排除维修系统，其特征在于：包括：

虚拟环境构建模块，用于基于目标船舶的基本信息，构建目标船舶虚拟环境，进而基于其并结合目标船舶故障的基本信息，构建目标船舶虚拟环境中各类型所属各船舶机电装备故障模拟状态，进一步将目标船舶虚拟环境以及其中各类型所属各船舶机电装备故障模拟状态统称为目标船舶机电装备虚拟环境；

虚拟环境校验模块，用于获取目标船舶机电装备虚拟环境的对比信息，分析目标船舶机电装备虚拟环境的评价情况，若其为合格，则执行故障排除维修启动模块，若其为不合格，则执行虚拟环境构建模块；

故障排除维修启动模块，用于各维修人员根据预定义原则启动目标船舶机电装备虚拟环境，进行故障排除维修模拟操作和学习；

故障排除维修分析模块，用于获取各维修人员当前故障排除维修测试对应各故障模拟状态的过程信息，分析各维修人员当前故障排除维修测试对应各故障模拟状态的评价指标，将其进行反馈；

故障排除维修解析模块，用于从信息库中提取各维修人员各次故障排除维修测试对应各故障模拟状态的评价指标，分析各维修人员的故障排除维修测试对应故障模拟状态的变化趋势指标以及各维修人员的故障排除维修测试对应各类型故障模拟状态的评价指标；

评估反馈模块，用于分析各维修人员的故障排除维修测试的综合评价情况；

信息库，用于存储各维修人员各次故障排除维修测试的过程信息和评价指标，存储维修人员各次故障排除维修测试对应各故障模拟状态的标准过程信息。

2.根据权利要求1所述的一种船舶机电装备虚拟环境中故障排除维修系统，其特征在于：所述目标船舶的基本信息包括设计图纸和技术文档；

所述目标船舶故障的基本信息包括故障资料和故障案例；

所述目标船舶机电装备虚拟环境的对比信息包括船舶相似度和各类型所属各船舶机电装备故障相似度；

所述各维修人员当前故障排除维修测试对应各故障模拟状态的过程信息包括故障排查顺序符合度、故障排查结论准确度、维修操作顺序符合度、维修操作规范度和维修操作准确度。

3.根据权利要求2所述的一种船舶机电装备虚拟环境中故障排除维修系统，其特征在于：所述目标船舶虚拟环境的具体构建方式为：

A1、提取目标船舶的设计图纸和技术文档，在虚拟环境开发平台中，依据目标船舶的设计图纸中总体布置图，创建目标船舶虚拟环境的基础场景框架；

A2、依据目标船舶的设计图纸和技术文档中各船舶机电装备的设计图，创建目标船舶虚拟环境中各船舶机电装备的三维模型；

A3、依据目标船舶的设计图纸中船舶机电装备的布置图和装配图，在目标船舶虚拟环境的基础场景框架中将各船舶机电装备进行装配和连接，进而得到目标船舶虚拟环境；

A4、开发维修人员与目标船舶虚拟环境之间的交互功能。

4.根据权利要求3所述的一种船舶机电装备虚拟环境中故障排除维修系统，其特征在于：所述目标船舶虚拟环境中各类型所属各船舶机电装备故障模拟状态的构建方式为：

D1、提取目标船舶故障的故障资料和故障案例，对其进行梳理得到目标船舶的各类型所属各船舶机电装备故障以及其产生机制、触发条件以及对设备自身和关联设备的影响；

D2、利用虚拟开发平台的脚本编程或者相关插件功能，根据目标船舶的各类型所属各船舶机电装备故障以及其产生机制、触发条件以及对设备自身和关联设备的影响，在目标船舶虚拟环境中进行故障模拟构建，得到目标船舶虚拟环境中各类型所属各船舶机电装备故障模拟状态。

5.根据权利要求2所述的一种船舶机电装备虚拟环境中故障排除维修系统，其特征在于：所述目标船舶机电装备虚拟环境的评价情况的具体分析方式为：

提取目标船舶机电装备虚拟环境的船舶相似度和各类型所属各船舶机电装备故障相似度，分别记为$$
Ship, ~ Fault_{jb}$$，其中$$
j=1, 2,..., J
$$，$$
j
$$为各类型的编号，$$
J
$$为类型的数量，$$
b=1, 2,...., B
$$，$$
b
$$为各船舶机电装备故障的编号，$$
B
$$为船舶机电装备故障的数量，分析目标船舶机电装备虚拟环境的评价指标$$
Evaluate=\beta_{1}^{\ast}Ship+\beta_{2}^{\ast}\sum_{j=1}^{J}\sum_{b=1}^{B}Fault_{jb}$$，其中$$\beta_{1}, ~\beta_{2}$$分别为设定的船舶相似度和船舶机电装备故障相似度对应评价指标的权重因子；

将目标船舶机电装备虚拟环境的评价指标与设定的评价指标阈值进行对比，若目标船舶机电装备虚拟环境的评价指标大于评价指标阈值，则将目标船舶机电装备虚拟环境的评价情况记为合格，反之，则将目标船舶机电装备虚拟环境的评价情况记为不合格。

6.根据权利要求1所述的一种船舶机电装备虚拟环境中故障排除维修系统，其特征在于：根据预定义原则启动目标船舶机电装备虚拟环境的内容为：各维修人员根据自己的故障排除维修水平进行自行选择故障排除维修测试，进而在目标船舶机电装备虚拟环境中进行启动和确认操作。

7.根据权利要求2所述的一种船舶机电装备虚拟环境中故障排除维修系统，其特征在于：所述各维修人员当前故障排除维修测试对应各故障模拟状态的评价指标的具体分析方式为：

提取各维修人员当前故障排除维修测试对应各故障模拟状态的故障排查顺序符合度、故障排查结论准确度、维修操作顺序符合度、维修操作规范度和维修操作准确度，分别记为$$
Bug_{fg}^{1}, ~ Bug_{fg}^{2}, ~ Bug_{fg}^{3}, ~ Bug_{fg}^{4}, ~ Bug_{fg}^{5}$$，其中$$
f=1, 2,..., c
$$，$$
f
$$为各维修人员的编号，$$
c
$$为维修人员的数量，$$
g=1, 2,..., G
$$，$$
g
$$为各故障模拟状态的编号，$$
G
$$为故障模拟状态的数量，分析各维修人员当前故障排除维修测试对应各故障模拟状态的评价指标$$
Index_{fg}=\operatorname{tanh}\left(\frac{Bug_{fg}^{1}}{Bug_{0}^{1}}+Bug_{fg}^{2}+\frac{Bug_{fg}^{3}}{Bug_{0}^{3}}+\frac{Bug_{fg}^{4}}{Bug_{0}^{4}}+\frac{Bug_{fg}^{5}}{Bug_{0}^{5}}\right)
$$，其中$$
Bug_{0}^{1}, ~ Bug_{0}^{3}, ~ Bug_{0}^{4}, ~ Bug_{0}^{5}$$分别为预置的维修人员当前故障排除维修测试对应故障模拟状态的故障排查顺序符合度阈值、维修操作顺序符合度阈值、维修操作规范度阈值和维修操作准确度阈值。

8.根据权利要求7所述的一种船舶机电装备虚拟环境中故障排除维修系统，其特征在于：所述各维修人员的故障排除维修测试对应故障模拟状态的变化趋势指标的具体分析方式为：

提取各维修人员各次故障排除维修测试对应各故障模拟状态的评价指标$$\boldsymbol{Index}_{fqg}^{\prime}$$，其中$$
q=1, 2,..., Q
$$，$$
q
$$为各次故障排除维修测试的编号，$$
Q
$$为故障排除维修测试的次数，分析各维修人员的故障排除维修测试对应故障模拟状态的变化趋势指标$$
Trend_{f}=\sum_{q=1}^{Q-1}\!\!\left[\frac{1}{G}\sum_{g=1}^{G}Index_{f ( q+1 ) g}^{\prime}-\frac{1}{G}\sum_{g=1}^{G}Index_{fqg}^{\prime}\right]
$$，其中$$\boldsymbol{Index}_{f ( q+1 ) g}^{\prime}$$为第$$
f
$$个维修人员第$$
( q+1 )
$$次故障排除维修测试对应第$$
g
$$个故障模拟状态的评价指标。

9.根据权利要求8所述的一种船舶机电装备虚拟环境中故障排除维修系统，其特征在于：所述各维修人员的故障排除维修测试对应各类型故障模拟状态的评价指标的具体分析方式为：

提取各维修人员各次故障排除维修测试对应各故障模拟状态的评价指标，将其根据故障模拟状态类型进行归类得到各维修人员的故障排除维修测试对应各类型故障模拟状态所属各故障模拟状态的评价指标$$
Index_{fph}^{\prime\prime}$$，其中$$
p=1, 2,..., d
$$，$$
p
$$为各类型故障模拟状态的编号，$$
d
$$为故障模拟状态的类型数，$$
h=1, 2,..., H
$$，$$
h
$$为类型故障模拟状态所属各故障模拟状态的编号，$$
H
$$为类型故障模拟状态所属故障模拟状态的数量；

分析各维修人员的故障排除维修测试对应各类型故障模拟状态的评价指标$$
Sim_{fp}=\frac{1}{H}\sum_{h=1}^{H}Index_{fph}^{\prime\prime}$$。

10.根据权利要求9所述的一种船舶机电装备虚拟环境中故障排除维修系统，其特征在于：所述各维修人员的故障排除维修测试的综合评价情况的具体分析方式为：

提取各维修人员的故障排除维修测试对应故障模拟状态的变化趋势指标，若某维修人员的故障排除维修测试对应故障模拟状态的变化趋势指标大于0，则将该维修人员在故障排除维修测试中故障排除和维修能力情况记为逐渐提升，反之，则将该维修人员在故障排除维修测试中故障排除和维修能力情况记为未提升；

提取各维修人员的故障排除维修测试对应各类型故障模拟状态的评价指标，从中筛选得到类型故障模拟状态的评价指标大于设定的类型故障模拟状态的评价指标阈值的各维修人员的故障排除维修测试对应各类型故障模拟状态，将其记为各维修人员的故障排除维修测试对应各擅长类型故障模拟状态；

进一步将各维修人员在故障排除维修测试中故障排除和维修能力情况以及各维修人员的故障排除维修测试对应各擅长类型故障模拟状态统称为各维修人员的故障排除维修测试的综合评价情况。



