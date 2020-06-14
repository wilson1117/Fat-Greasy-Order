## intent: startOrder
- 點餐

## intent: foodOrder
- [鳳梨披薩](food)
- [珍珠披薩](food)
- [臭豆腐雞排](food)
- [吉娃娃絲襪奶茶](food)
- [古早味阿嬤紅茶](food)
- [手工熬煮冬瓜茶](food)
- [肥宅快樂水](food)
- [心痛痛的滋味](food)


## intent: foodCount
- [1](count)個
- [1](count)杯

## intent: foodOrder+foodCount
- 我要[1](count)個[鳳梨披薩](food)
- 我要[3](count)份[鳳梨披薩](food)
- [2](count)杯[手工黑糖冬瓜茶](food)
- [3](count)片[珍珠披薩](food)
- 我要[1](count)杯[吉娃娃絲襪奶茶](food)


## intent: ice_select
- 冰塊[正常](ice_type)
- [少冰](ice_type)
- 我要[少冰](ice_type)
- [微冰](ice_type)
- 我要[微冰](ice_type)
- [去冰](ice_type)
- 我要[去冰](ice_type)

## intent: sugar_select
- 甜度[台南](sugar_type)
- 我要[台南]甜度(sugar_type)
- [正常](sugar_type)甜
- [全糖](sugar_type)
- 我要[全糖](sugar_type)
- [半糖](sugar_type)
- 我要[半糖](sugar_type)
- [微糖](sugar_type)
- 我要[微糖](sugar_type)
- [無糖](sugar_type)
- 我要[無糖](sugar_type)

## intent: ice_select+sugar_select
- [半糖](sugar_type)[少冰](ice_type)
- [微糖](sugar_type)[去冰](ice_type)
- [全糖](sugar_type)[正常](ice_type)
- [半糖](sugar_type)[少冰](ice_type)
- [半](sugar_type)[少](ice_type)
- [全](sugar_type)[微](ice_type)
- [半](sugar_type)[去](ice_type)
- [台南](sugar_type)[去冰](sugar_type)

## intent: size_select
- [大杯](size)
- [中杯](size)
- [小杯](size)
- 我要[大杯]的(size)
- 我要[中杯]的(size)
- 我要[小杯]的(size)
- [大的](size)
- [中的](size)
- [小的](size)
- 我要[大的](size)
- 我要[中的](size)
- 我要[小的](size)

## intent: want_finish
- 這樣就好
- 結束點餐
- 這樣就好了
- 這樣就好了謝謝
- 就這些

## intent: response_check
- 沒錯
- 是的
- 正確
- 沒問題

## synonym:半糖
- 半
- 半糖

## synonym:全糖
- 全
- 全糖
- 正常

## synonym:少糖
- 少
- 少糖

## synonym:無糖
- 無糖
- 無

## synonym:微冰
- 微
- 微冰

## synonym:正常冰
- 正常
- 正常冰

## synonym:少冰
- 少
- 少冰

## synonym:去冰
- 去冰
- 去

## synonym:大杯
- 大杯
- 大
- 大的

## synonym:中杯
- 中杯
- 中
- 中的
- 不大不小

## synonym:小杯
- 小杯
- 小
- 小的