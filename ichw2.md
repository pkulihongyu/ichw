# ichw2


---


### *1. 用你的语言描述图灵为什么要证明停机问题,其证明方法和数学原理是什么.*

**目的**：说明存在不可计算问题（不是所有的问题都能用图灵机解决）（存在不能“有效计算”的函数）

**证明方法：反证法**

假设对于任意程序及程序的任意输入，存在一个“上帝算法”可以判定程序是否终止（图灵机是否停机）
```
def god(program, input):
	if (program halts on input):
		return True
	else:
        	return False
```
现在构造一个“撒旦算法”，它借助于前述的“上帝算法”
```
def satan(program):
	if god(program, program):
		loop forever
		return False    #这一条代码不会被执行
	else:
		return True
```
现在构造矛盾：令“撒旦算法”调用它自己
```
satan(santa)
```
若`santa(santa)`能够停机，则`god(santa, santa)`返回`True`，程序进入第一条分支，`santa(santa)`不会停机；
若`santa(santa)`不能停机，则`god(santa, santa)`返回`False`，程序进入第二条分支，`santa(santa)`返回`True`，而后程序停机。
发生矛盾，从而证明了能判定任意程序终止性的“上帝算法”并不存在。

**数学原理：康托尔对角线方法**

假设我们可以将任意图灵机**Ti**在任意可能输入**Ii**下是否停机的情况列成一张表（基于图灵机的可列性）：

|halt|I1|I2|I3|…|In|…|
|---|---|---|---|---|---|---|
|T1|n|y|n|…|y|…|
|T2|y|n|n|…|y|…|
|T3|y|y|y|…|y|…|
|…|
|Tn|n|n|n|…|y|…|
|…|

现在构造一台新的图灵机**P**，它与图灵机**Tk**在输入**Ik**下的停机状况不同，即
```
if Tk(Ik) == y:
	P(Ik) = n
else:
	P(Ik) = y
```
那么P与以上任意一台图灵机均不同。这说明我们并不能判定所有图灵机的停机情况，即“停机问题”不可解。 


---


### *2. 你在向中学生做科普，请向他们解释二进制补码的原理.*

在减去正数（加上负数）时,

![](http://latex.codecogs.com/gif.latex?\\X-Y=X+(-Y)=X+(2^N-Y)-2^N)

（其中N表示ALU的位长）
由于溢出，最后一项![](http://latex.codecogs.com/gif.latex?\\2^N)被自动减去。
由此我们看到，若将负数-Y以![](http://latex.codecogs.com/gif.latex?\\2^N-Y)的形式表示，即可将减法转化为加法，计算可得到正确结果。

因此按如下方式定义X的补码：

![](http://latex.codecogs.com/gif.latex?\\[X]=\left\{\begin{array}{l@{\quad:\quad}l}X&0≤X≤2^{N-1}-1\\2^N-|X|&-2^{N-1}≤X<0\end{array}\right.)

通过解释器/编译器将负数以二进制补码的形式表示，可以巧妙利用溢出，实现加法和减法的统一，简化CPU的电路设计。

例如，在4-bit的计算机上计算4-3：（最后一步-16由溢出自动实现）
```
4-3 = 4+(-3) = 4+(16-3)-16
0100+1101 = 10001(overflow) = 0001
即 4+(-3) = 1
```

（注：若溢出未实际发生，则需要解释器/编译器将得到的首位为1的二进制补码再次取补，从而得到原码：

![](http://latex.codecogs.com/gif.latex?\\X-Y=X+(2^N-Y)-2^N=-(2^N-(X+(2^N-Y))))

例如，在4-bit的计算机上计算3-5：
```
3-5 = 3+(-5) = 3+(16-5)-16
0011+1011 = 1110(取补码) = -(10000-1110) = -0002
即3-5 = -2
```
）


---


### *3. 某基于 IEEE 754浮点数格式的 16 bit 浮点数表示, 有 8 个小数位, 请给出 ±0, ±1.0, 最大非规范化数, 最小非规范化数, 最小规范化浮点数, 最大规范化浮点数, ±∞, NaN 的二进制表示(表示形式请参照讲义).*

|数字|sign|exp|frac|value|
|---|---|---|---|---|
|±0.0 |*|0000000|00000000|
|±1.0|*|0111111|00000000|
|最大非规范化数|*|0000000|11111111|![](http://latex.codecogs.com/gif.latex?\\±(1-2^{-8})*2^{-62}})
|最小非规范化数|*|0000000|00000001|![](http://latex.codecogs.com/gif.latex?\\±2^{-8}*2^{-62})
|最小规范化浮点数|*|0000001|00000000|![](http://latex.codecogs.com/gif.latex?\\±2^{-62})
|最大规范化浮点数|*|1111110|11111111|![](http://latex.codecogs.com/gif.latex?\\±(2-2^{-8})*2^{63})
|±∞|*|1111111|00000000|
|NaN|*|1111111|Non Zero|

注：sign位正数为0，负数为1

---

>参考文献：
[1][裘宗燕， 什么是计算](http://www.math.pku.edu.cn/teachers/qiuzy/computing/courseware/lecture07-computing1.pdf)
[2][刘未鹏， 康托尔、哥德尔、图灵——永恒的金色对角线(rev#2)](http://mindhacks.cn/2006/10/15/cantor-godel-turing-an-eternal-golden-diagonal/)
[3][guoshuaia， 整数二进制补码的数学原理(two's complement)](http://www.360doc.com/content/16/0809/10/35391156_581862685.shtml)
[4][曹东刚， 数据及其表示](https://caodg.github.io/ic/slides/02.data/#40)

>说明：
本文原使用“作业部落 cmd markdown 编辑阅读器”写就，通过Git上传到GitHub，但由于作者的疏忽以及GitHub与本地编辑器可能存在的不同，文章中出现多处排版混乱，如含有括号的句子不能正确倾斜、列表错乱、使用LaTeX渲染的公式显示原码、进行页内跳转的超链接不能正确工作等。虽然作者耗费大量精力，多方查找资料尽力修复，但仍有多处错误不能很好地解决。
不便阅读之处，望各位读者海涵。也希望各位读者能提出有效的解决方案，作者将不胜感谢！

>致谢：
本文中的LaTeX公式渲染方法来自网络，在此感谢知乎网友@Deep Reader的方法，链接https://www.zhihu.com/question/26887527/answer/43166739


