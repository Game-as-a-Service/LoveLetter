# created by Fu at 2022/11/30
Feature: 王子 出牌規則

  Scenario: 玩家出王子 指定一位其他玩家後出牌
    Given 玩家A 持有 王子
    Given 玩家B 持有 王子
    When 玩家A 對 玩家B 出牌 王子
    Then 玩家B 丟棄手牌
    Then 玩家B 從牌庫拿一張牌

  Scenario: 玩家出王子 指定自己後出牌
    Given 玩家A 持有 王子
    When 玩家A 對 自己 出牌 王子
    Then 玩家A 丟棄手牌
    Then 玩家B 從牌庫拿一張牌

# TODO: 牌庫沒有牌的function，從移除牌拿牌的function
#  Scenario: 玩家出王子 指定沒有手牌的玩家後出牌
#    Given 玩家A 持有 王子
#    Given 牌庫 已經沒有牌
#    When 玩家A 對 玩家B 出牌 王子
#    Then 玩家B 丟棄手牌
#    Then 玩家B 從 移除牌 拿取一張牌

  Scenario: 玩家出王子 指定已經被侍女保護的人
    Given 玩家A 持有 王子
    Given 玩家B 被侍女保護中
    When 玩家A 對 玩家B 出牌 王子
    Then 玩家B 丟棄手牌
    Then 玩家B 從牌庫拿一張牌
