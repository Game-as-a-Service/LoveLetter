# created by Zeng at 2022/11/29
Feature: 公主 出牌規則

  Scenario: 玩家出牌 玩家出局
    Given 玩家A 持有 公主 王子
    When 玩家A 出牌 公主
    Then 玩家A 出局

  Scenario: 玩家被迫出牌 玩家出局
    Given 玩家A 持有 王子 國王
    Given 玩家B 持有 公主
    When 玩家A 對 玩家B 出牌 王子
    Then 玩家B 丟棄手牌
    Then 玩家B 出局