Feature: 衛兵 出牌規則

  Scenario: 玩家出牌 猜中對手的牌
    Given 玩家A 持有 衛兵 男爵
    Given 玩家B 持有 神父
    When 玩家A 對 玩家B 出牌 衛兵 指定 神父
    Then 玩家B 出局

  Scenario: 玩家出牌 沒猜中對手的牌
    Given 玩家A 持有 衛兵 男爵
    Given 玩家B 持有 神父
    When 玩家A 對 玩家B 出牌 衛兵 指定 公主
    Then 玩家B 未出局

  Scenario: 玩家出牌 對手被侍女保護中
    Given 玩家A 持有 衛兵 男爵
    Given 玩家B 被侍女保護中
    When 玩家A 對 玩家B 出牌 衛兵 指定 神父
    Then 玩家B 未出局

  Scenario: 玩家出牌 猜對手為衛兵不合規則
    Given 玩家A 持有 衛兵 男爵
    Given 玩家B 持有 神父
    Then 玩家A 對 玩家B 出牌 衛兵 無法指定 衛兵