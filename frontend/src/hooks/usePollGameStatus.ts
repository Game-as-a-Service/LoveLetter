import { getGameStatus } from "@/apis";
import { GameStatus } from "@/types";
import isEqual from "lodash/isEqual";
import { useCallback, useEffect, useState } from "react";

/** Keep game status updated by polling. */
export function usePollGameStatus(gameId: string, username: string) {
  // TODO: break down GameStatus to separate states.
  const [gameStatus, setGameStatus] = useState<GameStatus | null>(null);

  const getCurrentGameStatus = useCallback(() => {
    return getGameStatus(gameId, username).then((status: GameStatus) => {
      setGameStatus((currentStatus) =>
        !isEqual(currentStatus, status) ? status : currentStatus
      );
    });
  }, [gameId, username]);

  // refresh GameStatus every 1 second.
  useEffect(() => {
    // set GameStatus before the refresher triggered
    getCurrentGameStatus();

    const intervalId = setInterval(() => {
      // auto-refresh GameStatus
      getCurrentGameStatus();
    }, 1 * 1000);
    return () => {
      clearInterval(intervalId);
    };
  }, [getCurrentGameStatus]);

  return gameStatus;
}
