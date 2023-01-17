import { Button, Flex, Input, Spacer } from "@chakra-ui/react";
import React, { useEffect } from "react";

import { useGameId, useUsername } from "../hooks";
import { ViewState } from "../types";
import { IsGameAvailable, JoinGame } from "../apis";

export function CreateOrJoinGame(props: {
  visitFunc: (view: ViewState) => void;
}) {
  const [username, setUsername] = useUsername();
  const [roomId, setRoomId] = useGameId();

  useEffect(() => {
    // clean up the roomId at the beginning when it is not available.
    if (roomId !== "") {
      IsGameAvailable(roomId, username).then((result: boolean) => {
        if (!result) {
          setRoomId("");
        }
      });
    }
  }, []);

  return (
    <>
      <Flex
        bg="red.50"
        height="100vh"
        justifyContent="center"
        alignItems="center"
      >
        <Flex
          bg="lightblue"
          height="33vh"
          width="33vw"
          rounded="1rem"
          p="3"
          direction="column"
        >
          <Flex m={3}>輸入遊戲資訊</Flex>
          <Flex m={3} direction="column">
            <Input
              mb={2}
              type="text"
              bg="blue.200"
              placeholder="玩家名稱"
              value={username}
              _placeholder={{ color: "gray.500" }}
              onChange={(e) => {
                setUsername(e.target.value);
              }}
            ></Input>
            <Input
              type="text"
              bg="blue.200"
              placeholder="房間代號"
              value={roomId}
              _placeholder={{ color: "gray.500" }}
              onChange={(e) => {
                setRoomId(e.target.value);
              }}
            ></Input>
          </Flex>
          <Spacer />
          <Flex m={3} alignSelf="flex-end">
            <Button
              mr={5}
              rounded="5px"
              bg="blue.700"
              color="blue.50"
              _hover={{ color: "yellow.500" }}
              onClick={() => {
                JoinGame(roomId, username).then((result: boolean) => {
                  if (result === false) {
                    alert("遊戲無法加入");
                  } else {
                    props.visitFunc("game-room");
                  }
                });
              }}
            >
              加入遊戲
            </Button>
            <Button
              rounded="5px"
              bg="blue.700"
              color="blue.50"
              _hover={{ color: "yellow.500" }}
              onClick={() => {
                // props.visitFunc("game-list");
              }}
            >
              建立遊戲
            </Button>
          </Flex>
        </Flex>
      </Flex>
    </>
  );
}
