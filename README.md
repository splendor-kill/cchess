# cchess

### TODO

- [ ] env

  - [ ] GUI
  - [x] action 引起将帅碰面
  - [x] action 引起被将军
  - [ ] 结束条件（求和）
  - [ ] UCCI

- [ ] baseline

  - [ ] alpha-beta search
  - [ ] 监督学习
    - [x] [数据集](https://www.kaggle.com/boyofans/onlinexiangqi)
    - [ ] [爬虫](xqbase.com)

- [ ] benchmark

- [ ] pipeline

  - [ ] contribute
  - [ ] match
  - [ ] self-play
  - [ ] analysis
  - [ ] commucation protocol
  - [ ] hyper params opt

- [ ] model

- [ ] MCTS

- [ ] 实验

  - [ ] state用己方视角表示或用中立表示是否有不同？
  
- [ ] src

  - [x] leela zero
  - [ ] Stockfish
  - [x] ELF OpenGo
  - [x] KataGo

  

  

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



### reference

* [Xiangqi](https://en.wikipedia.org/wiki/Xiangqi)

* [中式记法](https://zh.wikipedia.org/wiki/%E8%B1%A1%E6%A3%8B) [西式记法](http://wxf.ca/xq/computer/wxf_notation.html) [着法表示](https://www.xqbase.com/protocol/cchess_move.htm)

* [术语](http://wxf.ca/xq/computer/XIANGQI_TERMS_IN_ENGLISH.pdf)

* [UCCI](https://www.xqbase.com/protocol/cchess_ucci.htm) [UCI](https://gist.github.com/aliostad/f4470274f39d29b788c1b09519e67372)

* [Elo计算](https://www.xqbase.com/protocol/elostat.htm)

* [源码](https://github.com/Zeta36/chess-alpha-zero.git)

  

