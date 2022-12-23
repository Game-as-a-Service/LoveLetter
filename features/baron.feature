# Created by Ian at 2022/12/23
Feature: 伯爵 出牌規則

  Scenario: 玩家出伯爵 指定一位其他玩家後出牌
    Given 玩家A 持有 男爵
    Given 玩家B 持有 神父
    When 玩家A 對 玩家B 出牌 男爵
    Then 玩家B 丟棄手牌
    Then 玩家B 出局

  Scenario: 玩家出伯爵 指定一位其他玩家後出牌
    Given 玩家A 持有 男爵
    Given 玩家B 持有 侍女
    When 玩家A 對 玩家B 出牌 男爵
    Then 玩家A 丟棄手牌
    Then 玩家A 出局

  Scenario: 玩家出伯爵 指定已經被侍女保護的人
    Given 玩家A 持有 男爵
    Given 玩家B 持有 神父
    Given 玩家B 被侍女保護中
    When 玩家A 對 玩家B 出牌 男爵
    Then 玩家B 未出局
