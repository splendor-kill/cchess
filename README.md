# cchess

### TODO

- [ ] env

  - [ ] GUI
  - [x] action 引起将帅碰面
  - [x] action 引起被将军
  - [ ] 结束条件（求和）

- [ ] baseline

  - [ ] alpha-beta search
  - [ ] 监督学习

- [ ] benchmark

- [ ] pipeline

- [ ] model

- [ ] MCTS

- [ ] 实验

  - [ ] state用己方视角表示或用中立表示是否有不同？
  - [ ] 

  



### Design decisions

#### observation

以当前玩家的视角观察，包括坐标系、行、列，以及当前的合法走法



#### action

以当前玩家的视角行动，action space: `MultiDiscrete(9, 10, 9, 10)`

前面2维表示源位置`(col, row)`，后面2维表示目标位置

**注意**：

* 策略应该包含对对手求和请求的处理，回答是否同意和





### 环境使用

```python

```



### AlphaZero

$(\mathbf{p}, v)=f_{\theta}(s)$

$p_{a}=\operatorname{Pr}(a \mid s)$

$v \approx \mathbb{E}[z \mid s]$

$l=(z-v)^{2}-\boldsymbol{\pi}^{\top} \log \mathbf{p}+c\|\theta\|^{2}$

使用单个连续更新的NN

使用Bayesian优化调参，并且使用相同的超参，例外是noise，为保证探索性，与合法招数成比例。

actions编码为spatial planes 或一个向量

训练70万步，batch size 4096，5000 TPUv1 生成self-play 对局，64 TPUv2训练网络

300k步的时候超过Stockfish，110k步超过Elmo，165k步超过AlphaGo Lee

AlphaZero和AlphaGo Zero 跑在一台4 TPU的机器上，Stockfish和Elmo使用最强水平(64线程和hash大小1G)

AlphaZero 在chess中每秒只搜80k 局面，在shogi中搜40k，作为对比，Stockfish 70M/s，Elmo 35M/s。即AlphaZero更像人

输入带8步历史，以当前玩家视角描述，每种棋子一个面，常量值面表示玩家颜色、总行动数和特殊规则的状态。

chess的行动分2个部分：先选子，再选其合法走法。chess和shogi的action表示为plane，围棋的表示为向量，但都表示为向量也可以，只是稍慢。如chess的action shape是$8\times 8\times 73$，前面的$8\times8$表示选子的位置

非法的走法通过把概率设为0屏蔽掉，再把剩下合法走法re-normalising成一个概率分布。



训练时每个MCTS使用800次模拟，其它根据游戏不同而不同。learning rate：0.2，0.02，0.002，0.0002

根节点加入Dirichlet noise $\operatorname{Dir}(\alpha)$ 到先验分布，其参数 $\alpha$ 与合法步数近似成反比。



评估时，根据根访问计数贪心选择走法。再4 TPU 单机上跑。

以Elo评级玩家水平，$a$打败$b$的概率：$p(a \text{ defeats } b)=\frac{1}{1+\exp \left(c_{\mathrm{elo}}(e(b)-e(a))\right.}$，其中 $c_{\mathrm{elo}}= 1/400$

$e(\cdot)$ 是通过 *BayesElo* 计算出的Bayesian logistic regression

每步允许想1分钟









### reference

* [中式记法](https://zh.wikipedia.org/wiki/%E8%B1%A1%E6%A3%8B)
* [西式记法](http://wxf.ca/xq/computer/wxf_notation.html)

* [术语](http://wxf.ca/xq/computer/XIANGQI_TERMS_IN_ENGLISH.pdf)

  

