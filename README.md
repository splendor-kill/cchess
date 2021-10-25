# cchess

### Design decisions



#### observation

以当前玩家的视角观察，包括坐标系、行、列，以及当前的合法走法





#### action

以当前玩家的视角行动，action space: `MultiDiscrete(9, 10, 9, 10)`

前面2维表示源位置`(col, row)`，后面2维表示目标位置

**注意**：

* 策略应该包含对对手求和请求的处理，回答是否同意和
* 



### TODO

- [ ] env
  - [ ] GUI
  - [x] action 引起将帅碰面
  - [ ] action 引起被将军
  - [ ] 结束条件（求和）
- [ ] model
- [ ] MCTS
- [ ] 





### reference

* [中式记法](https://zh.wikipedia.org/wiki/%E8%B1%A1%E6%A3%8B)
* [西式记法](http://wxf.ca/xq/computer/wxf_notation.html)

* [术语](http://wxf.ca/xq/computer/XIANGQI_TERMS_IN_ENGLISH.pdf)

  

