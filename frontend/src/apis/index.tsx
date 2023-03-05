import axios, { RawAxiosRequestHeaders } from "axios";

import { isEmpty } from "lodash";
import { GameStatus } from "@/types";
import * as process from "process";

export const defaultHeaders: RawAxiosRequestHeaders = {
  Accept: "application/json",
  "Content-Type": "application/json",
};

const BACKEND_URL =
  process.env.REACT_APP_BACKEND_API || "http://127.0.0.1:8080";

export const backendAxios = axios.create({
  baseURL: BACKEND_URL,
  // TODO how to set CORS correctly?
  // withCredentials: typeof window !== undefined ? true : false, // It will attach cookie for each request.
  headers: defaultHeaders,
});

export async function IsGameAvailable(
  gameId: string,
  playerId: string
): Promise<boolean> {
  try {
    const response = await backendAxios.get<GameStatus>(
      `/games/${gameId}/player/${playerId}/status`
    );
    return response.data.game_id != null;
  } catch (e) {
    console.log(e);
    return false;
  }
}

export async function JoinGame(
  gameId: string,
  playerId: string
): Promise<boolean> {
  try {
    const response = await backendAxios.post<boolean>(
      `/games/${gameId}/player/${playerId}/join`
    );
    return response.data;
  } catch (e) {
    console.log(e);
    return false;
  }
}

export async function GetGameStatus(
  gameId: string,
  playerId: string
): Promise<GameStatus> {
  const response = await backendAxios.get<GameStatus>(
    `/games/${gameId}/player/${playerId}/status`
  );
  return response.data;
}

export async function StartGame(gameId: string): Promise<boolean> {
  const response = await backendAxios.post<boolean>(`/games/${gameId}/start`);
  return response.data;
}

export async function CreateGame(username: string): Promise<string> {
  const response = await backendAxios.post<string>(
    `/games/create/by_player/${username}`
  );
  return response.data;
}

export async function PlayCard(
  gameId: string,
  username: string,
  card: string,
  payload: { [prop: string]: string }
): Promise<GameStatus> {
  const response = await backendAxios.post<GameStatus>(
    `/games/${gameId}/player/${username}/card/${card}/play`,
    isEmpty(payload) ? null : payload
  );
  return response.data;
}
