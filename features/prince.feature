# created by Timk at 2022/12/2
Feature: 王子 出牌規則

#  TODO: 與牌庫相關的動作，等Deck完成後再實作
  Scenario: 玩家出王子 指定一位其他玩家後出牌
    Given 玩家A 持有 王子
    Given 玩家B 持有 王子
    When 玩家A 對 玩家B 出牌 王子
    Then 玩家B 丟棄手牌
#    Then 玩家B 從牌庫拿一張牌

#  TODO: 與牌庫相關的動作，等Deck完成後再實作
  Scenario: 玩家出王子 指定自己後出牌
    Given 玩家A 持有 王子
    When 玩家A 對 玩家A 出牌 王子
    Then 玩家A 丟棄手牌
#    Then 玩家A 從牌庫拿一張牌

  Scenario: 玩家出王子 指定已經被侍女保護的人
    Given 玩家A 持有 王子
    Given 玩家B 被侍女保護中
    When 玩家A 對 玩家B 出牌 王子
