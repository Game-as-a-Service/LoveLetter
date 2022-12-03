# created by Fu at 2022/12/2
Feature: 侍女 出牌規則

  Scenario: 玩家出侍女 擁有保護效果
    Given 玩家A 持有 神父 侍女
    When 玩家A 對 玩家A 出牌 侍女
    Then 玩家A 擁有保護效果