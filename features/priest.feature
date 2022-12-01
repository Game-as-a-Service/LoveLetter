# created by Fu at 2022/11/30
Feature: 神父 出牌規則

  Scenario: 玩家出神父 指定一位其他玩家後出牌
    Given 玩家A 持有 神父 衛兵
    Given 玩家B 持有 公主
    When 玩家A 對 玩家B 出牌 神父
    Then 玩家A 看到了 玩家B 的 公主
