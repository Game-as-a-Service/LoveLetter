Feature: 遊戲的固定規則

  https://github.com/Game-as-a-Service/LoveLetter/issues/19

  1. 遊戲需要由玩家建立
  2. 玩家建立遊戲即刻加入此遊戲之中
  3. 遊戲至少有 2 名玩家才能開始
  4. 遊戲最最多能有 4 名玩家，滿員後就無法再加入新玩家
  5. 遊戲開始後就無法再加入新玩家

  Scenario: 遊戲的建立到開始的規則

    Given 玩家A 建立遊戲
    When 玩家A 開始遊戲
    Then 遊戲無法開始，因為 Too Few Players

    Given 玩家B 加入遊戲
    When 玩家A 開始遊戲

    Then 遊戲已經開始
    Then 玩家C 無法加入遊戲，因為 Game Has Started

