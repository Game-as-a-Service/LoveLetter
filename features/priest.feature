# created by Fu at 2022/11/30
Feature: 神父 出牌規則

  Scenario: 玩家出神父 看到對手的手牌
    Given 玩家A 持有 神父 衛兵
    Given 玩家B 持有 公主
    When 玩家A 對 玩家B 出牌 神父
    Then 玩家A 看到了 玩家B 的 公主

  Scenario: 玩家出神父 對手被侍女保護中
    Given 玩家A 持有 神父 衛兵
    Given 玩家B 被侍女保護中
    When 玩家A 對 玩家B 出牌 神父
    Then 玩家A 什麼也沒看到
    Then 玩家A 剩一張手牌