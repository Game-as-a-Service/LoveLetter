# Created by Ian at 2022/12/23
Feature: 伯爵 出牌規則

  Scenario: 玩家出伯爵 指定玩家並使該玩家出局
    Given 玩家A 持有 男爵 國王
    Given 玩家B 持有 神父
    When 玩家A 對 玩家B 出牌 男爵
    Then 玩家B 出局

  Scenario: 玩家出伯爵 指定玩家 比較手牌後使自己出局
    Given 玩家A 持有 男爵 國王
    Given 玩家B 持有 伯爵夫人
    When 玩家A 對 玩家B 出牌 男爵
    Then 玩家A 出局

  Scenario: 玩家出伯爵 指定已經被侍女保護的人
    Given 玩家A 持有 男爵 國王
    Given 玩家B 持有 神父
    Given 玩家B 被侍女保護中
    When 玩家A 對 玩家B 出牌 男爵
    Then 玩家B 未出局
