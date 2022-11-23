# Created by eddy at 2022/11/23
Feature: 伯爵夫人 出牌規則

  Scenario: 玩家出牌 需出伯爵夫人
    Given 玩家A 持有 國王
    When 系統發牌給 玩家A 伯爵夫人
    Then 玩家A 成功打出 伯爵夫人

  Scenario: 玩家出牌 無法出國王
    Given 玩家A 持有 國王
    When 系統發牌給 玩家A 伯爵夫人
    Then 玩家A 無法打出 國王

  Scenario: 玩家出牌 需出伯爵夫人
    Given 玩家A 持有 王子
    When 系統發牌給 玩家A 伯爵夫人
    Then 玩家A 成功打出 伯爵夫人

  Scenario: 玩家出牌 無法出王子
    Given 玩家A 持有 王子
    When 系統發牌給 玩家A 伯爵夫人
    Then 玩家A 無法打出 王子
