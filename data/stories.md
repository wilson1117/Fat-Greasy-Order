## story_startOrder
* startOrder
  - action_start_order

## story_foodOrder
* foodOrder
  - utter_foodCount
* foodCount
  - action_food_order

## story_foodOrderFull
* foodOrder+foodCount
  - action_food_order

## story_ice_option
* ice_select
  - action_option_select

## story_sugar_option
* sugar_select
  - action_option_select

## story_ice_sugar_option
* ice_select+sugar_select
  - action_option_select

## story_size_select
* size_select
  - action_option_select

## story_order_finish
* want_finish
  - action_order_check
* response_check
  - action_send_order
