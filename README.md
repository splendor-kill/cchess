# cchess

## TODO

- [ ] baseline

  - [ ] alpha-beta search
  - [ ] 监督学习
    - [x] [数据集](https://www.kaggle.com/boyofans/onlinexiangqi)
    - [ ] [爬虫](xqbase.com)

- [ ] hyper params opt

- [ ] better model

  - [ ] transformer, embedding pieces

- [ ] 实验

  - [ ] state用己方视角表示或用中立表示是否有不同？
  - [ ] 不同action表示有什么影响？
  - [ ] 可变的action space，即学习新的action
  - [ ] off-line RL

- [ ] adapt to docker + s3

  - [ ] multi evaluators, trainers
  - [ ] communication between docker containers

  

## 拿来

* [源码 chess-alpha-zero](https://github.com/Zeta36/chess-alpha-zero.git)

* [界面 xqwlight](https://github.com/xqbase/xqwlight.git)



## reference

* [Xiangqi](https://en.wikipedia.org/wiki/Xiangqi)

* [中式记法](https://zh.wikipedia.org/wiki/%E8%B1%A1%E6%A3%8B) [西式记法](http://wxf.ca/xq/computer/wxf_notation.html) [着法表示](https://www.xqbase.com/protocol/cchess_move.htm)

* [术语](http://wxf.ca/xq/computer/XIANGQI_TERMS_IN_ENGLISH.pdf)

* [UCCI](https://www.xqbase.com/protocol/cchess_ucci.htm) [UCI](https://gist.github.com/aliostad/f4470274f39d29b788c1b09519e67372)

* [Elo计算](https://www.xqbase.com/protocol/elostat.htm)

  
