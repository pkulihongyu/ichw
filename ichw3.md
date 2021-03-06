# ichw3

---

### *1. 详述通用的高速缓冲存储器结构及工作原理*

- **结构**：
    - 缓存存储体(高速存储器，Cache entry)：由若干存储单元组成，存储由主存读入的命令或数据及其地址。每个存储单元分为3部分：
        - 标签(tag)：存储数据在主存中的地址（的一部分）
        - 数据块(data block)：通常与主存存储单元长度一致，存储由主存读入的数据
        - 标志位(flag bits)：
            - 有效标志位(valid bit)：说明该数据块中是否存储了有效的数据
            - 重写标志位(dirty bit)：说明从主存中取得数据后是否进行过改动

    - <span id="jump1">地址转换部件(联想存储器，Address translation)：借助目录表，实现主存地址到缓存地址的转换。转换方式有多种：</span>
        - 全关联(fully associative)：缓存中某单元可能对应内存中任意一个单元
        - 直接映射(direct-mapped)：缓存单元地址与内存单元地址一一对应
        - 组关联方式(实例有two-way set associative等)：每个缓存地址单元对应多个内存地址单元

    - <span id="jump2">替换部件(替换逻辑电路)：若缓存中没有空白单元，则将主存中的数据写入缓存，覆盖部分原有数据，并替换联想存储器中的目录表。替换方法有多种：</span>
        - 随机(Rand)法：随机确定被替换的数据块
        - 先进先出(FIFO)法：优先替换最先被调入的数据块
        - 最少使用(LFU)法：优先替换访问次数最少的数据块
        - 最近最少使用(LRU)法：优先替换近期访问次数最少的数据块
    
    - 其他控制线路


- **工作原理**：

  - 缓存从内存中读入数据，存储在缓存存储体中，并按照某种算法规则（由地址转换部件的算法决定，[见上](#jump1)）在转换中形成目录表。
当CPU发出指令访问内存中某个寻址单位的数据时，将内存地址在联想存储器中转换为缓存中的对应地址，并在缓存中寻找相应数据。若命中，则CPU存取缓存；否则，将主存中的相应数据块存入缓存。若脱靶时缓存已满，则按照一定算法规则（由替换部件的算法决定，[见上](#jump2)）更新缓存中的数据。

---

### **曹老师上课时提到的思考题**
#### *1. 怎样设计缓存以提高数据命中率*

  应该选取合适的地址关联方式：

- 若采用全关联方式，每次寻址内存中的任意一条数据，都需要与联想存储器中的全部条目比较，速度慢、成本高、实现难度大；但关联方式灵活，命中率高，对缓存存储空间的利用率高。
- 若采用直接映射方式，每次寻址内存中任意一条数据时，都只需要比较内存中地址相同的条目，访问速度快、成本低、容易实现；但关联方式固定，容易出现“脱靶”的情况，导致缓存中的数据频繁被替换。
- 可以将以上两种方式结合，采取“组关联方式”，即将缓存单元和内存单元分别分组（组数相同），在缓存和主存的对应组之间采用直接映射方式，在组内采用全关联方式，这样兼具全关联方式命中率高和直接映射方式访问速度快的优点，但比较难以实现。

#### *2. 怎样更新缓存中的数据*
- 采用合理的预取(prefetch)方式：
    根据“局部性原理”，若某一存储单元中的数据正在被访问，则它（时间局部性）和它附近的单元（空间局部性）中的数据在近期很可能会被访问。因此，这些数据应该优先被预取到缓存中。
- 脱靶时若缓存已满，采用合理的数据覆盖方式（替换算法）：
    根据“时间局部性原理”，应该尽可能保留近期使用频率最高的数据，优先舍弃使用频率最低的数据，即采用“近期最少使用(LRU)算法”。

---

>参考文献：
[1][Wikipedia, CPU cache](https://en.wikipedia.org/wiki/CPU_cache#Cache_entry_structure)
[2][360百科, 高速缓冲存储器](https://baike.so.com/doc/6204325-6417592.html)

>说明：
本文原使用“作业部落 cmd markdown 编辑阅读器”写就，通过Git上传到GitHub，但由于作者的疏忽以及GitHub与本地编辑器可能存在的不同，文章中出现多处排版混乱，如含有括号的句子不能正确倾斜、列表错乱、使用LaTeX渲染的公式显示原码、进行页内跳转的超链接不能正确工作等。虽然作者耗费大量精力，多方查找资料尽力修复，但仍有多处错误不能很好地解决。
不便阅读之处，望各位读者海涵。也希望各位读者能提出有效的解决方案，作者将不胜感谢！
