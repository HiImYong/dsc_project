import React from 'react';
import { useDrag } from 'react-dnd';

const DraggableItem = ({ playerInfo }) => {
  const [, drag] = useDrag({
    type: 'PLAYER', // 드래그 타입. 각각을 식별하기 위한 타입을 설정합니다. 여기서는 'PLAYER'로 설정했습니다.
    item: { playerInfo },
  });

  return (
    <div ref={drag} style={{ cursor: 'move' }}>
      {`(${playerInfo.이름}:${playerInfo.팀}[게임수 : ${playerInfo.게임수}])`}
    </div>
  );
};

export default DraggableItem;