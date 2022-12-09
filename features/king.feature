# created by Fu at 2022/12/4
Feature: 國王 出牌規則

  Scenario: 玩家出國王 與指定玩家交換手牌
    Given 玩家A 持有 國王 侍女
    Given 玩家B 持有 王子
    When 玩家A 對 玩家B 出牌 國王
    Then 玩家A 手牌為 王子
    Then 玩家B 手牌為 侍女

  Scenario: 玩家出牌 對手被侍女保護中
    Given 玩家A 持有 男爵 國王
    Given 玩家B 持有 王子
    Given 玩家B 被侍女保護中
    When 玩家A 對 玩家B 出牌 國王
    Then 玩家A 手牌為 男爵
    Then 玩家B 手牌為 王子