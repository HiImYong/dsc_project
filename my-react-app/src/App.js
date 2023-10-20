// import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';


function App() {
  const 선수목록 = [
    '정재은','정관윤','우성재','조덕원','김유화','박청용','박은규','김좌순','김재식','홍정은','이익주','이상','박지영','유소이','박지훈', '유용재', '조태원'
  ];

  const [inputCount, setInputCount] = useState(14);
  const [inputData, setInputData] = useState(Array.from({ length: inputCount }, (_, i) => 선수목록[i] || ''));
    /*
  길이가 inputCount인 객체를 생성 -> Array.from에 의해 배열로 변환
  두 번째 매개변수는 매핑 함수(_는 현재 요소의 값, i는 현재 인덱스)
  선수목록[i] || ''는 선수목록 배열의 i번째 요소를 가져옴
  만약 해당 요소가 존재하지 않거나 값이 falsy (비어있는 문자열 포함)하면 빈 문자열('')을 사용.*/

  const [apiData, setApiData] = useState(null);

  // const [dragData, setDragData] = useState({});
  // const [dropData, setDropData] = useState({});

  let dragData;
  let dropData;

  const [ grab, setGrab ] = React.useState(null)
  const _onDragOver = e => {
    e.preventDefault();
}

const _onDragStart = e => {
  setGrab(e.target);
  console.log(e)
  console.log('드래그 TARGET : ', e.target)
  console.log('key :', e.target.getAttribute('data-pos'))
  console.log('row : ', e.target.getAttribute('data-row'))
  console.log('col : ', e.target.getAttribute('data-col'))
  
  let row = e.target.getAttribute('data-row')
  let col = e.target.getAttribute('data-col')
  let pos = e.target.getAttribute('data-pos')
  dragData = {"row" : row, "col" : col, "pos" : pos, "value" : apiData[row][col][pos]}
  
  e.target.classList.add("grabbing");
  e.dataTransfer.effectAllowed = "move";
  e.dataTransfer.setData("text/html", e.target);
}

const _onDragEnd = e => {
  e.target.classList.remove("grabbing");

  e.dataTransfer.dropEffect = "move";
  console.log('드래그종료')
}

const _onDrop = e => {

  console.log(e)
  console.log('드롭 TARGET : ', e.target)
  
  console.log('row : ', e.target.getAttribute('data-row'))  
  console.log('col : ', e.target.getAttribute('data-col'))
  console.log('pos :', e.target.getAttribute('data-pos'))

  let row = e.target.getAttribute('data-row')
  let col = e.target.getAttribute('data-col')
  let pos = e.target.getAttribute('data-pos')
  dropData = {"row" : row, "col" : col, "pos" : pos, "value" : apiData[row][col][pos]}

  if (dragData.value.팀 != dropData.value.팀){
    alert(`다른 팀 끼리는 위치변경이 불가합니다. '제출'을 눌러 다시 매치를 만들어주세요.`)
    return;
  }  

 for (const col of apiData[row]){
  for (const pos of col){
    if (dragData.value.이름 == pos.이름){
      if(dragData.row == dropData.row){
        continue;
      }
      else{
        alert(`해당 행에 이미 ${dragData.value.이름}님이 있습니다. 다시 배치해주세요.`)
      return;
      }
      
    }
  }
 }

  let copiedData = apiData;

  const updatedData = [...copiedData];

  updatedData[row][col][pos] = dragData.value
  updatedData[dragData.row][dragData.col][dragData.pos] = dropData.value

  setApiData(updatedData)

  
  if (!e.target) {
    console.error('드롭 대상이 없습니다.');
    return;
  }  




  // let _list = [ ...inputData ];
  // _list[grabPosition] = _list.splice(targetPosition, 1, _list[grabPosition])[0];

  // setInputData(_list);
}




  const handleInputChange = (index, value) => {
    setInputData((prevData) => { //  prevData는 현재 상태값인 inputData의 복사본
      const newData = [...prevData];
      newData[index] = value;
      return newData;
    });
  };




  const DraggableItem = ({ playerInfo, index, data_row, data_col }) => {
   
  
    return (
      <div
        draggable 
        onDragOver={_onDragOver}
        onDragStart={_onDragStart}
        onDragEnd={_onDragEnd}
        onDrop={_onDrop}
        ref={null} 

        key={index}

        data-pos={index}
        
        data-row={data_row}
        data-col={data_col}

        style={{ cursor: 'move',  margin:'3px'}}>
        {/* {`(${playerInfo.이름}:${playerInfo.팀}[게임수 : ${playerInfo.게임수}])`} */}
        {`(${playerInfo.이름}:${playerInfo.팀})`}
       
      </div>
      
    );
  };
  


  const handleAddInput = () => {
    setInputCount((prevCount) => prevCount + 1);
  };

  

  const handleSubmit = async  () => {

    for (let i = 0; i < inputData.length; i++) {
      if (inputData[i].trim() === '') {
        alert('값이 입력되지 않았습니다.');
        return; // 함수 종료
      }
    }

    const dataToSend = inputData.join(', ');
    // console.log(inputData);

    const apiUrl = 'http://127.0.0.1:5000/result';
    const urlWithQuery = apiUrl + '?data=' + encodeURIComponent(dataToSend);

    try {
      const response = await fetch(urlWithQuery);
  
      if (!response.ok) {
        throw new Error('네트워크 오류');
      }

      const result = await response.json();
        
            // API 응답(result)을 처리
            // console.log(result);
            var parsedData = JSON.parse(result);
            console.log(result)

            /*
          리스폰스 데이터형식  
          [ 
            row : 0 
            [  
              col : 0 [{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 1[{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 2[{key : 0}, {key : 1}, {key : 2}, {key : 3}]  
            ], 
            row : 1 
            [  
              col : 0 [{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 1[{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 2[{key : 0}, {key : 1}, {key : 2}, {key : 3}]  
            ], 
            row : 2 
            [  
              col : 0 [{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 1[{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 2[{key : 0}, {key : 1}, {key : 2}, {key : 3}]  
            ], 
            row : 3 
            [  
              col : 0 [{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 1[{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 2[{key : 0}, {key : 1}, {key : 2}, {key : 3}]  
            ], 
            row : 4 
            [  
              col : 0 [{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 1[{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 2[{key : 0}, {key : 1}, {key : 2}, {key : 3}]  
            ], 
            row : 5 
            [  
              col : 0 [{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 1[{key : 0}, {key : 1}, {key : 2}, {key : 3}] col : 2[{key : 0}, {key : 1}, {key : 2}, {key : 3}]  
            ], 
          ]
            */


          setApiData(parsedData)

          }
          catch (error) {
            console.error('API 요청 오류:', error);
          }

  };

  useEffect(() => {
    // 페이지 로드 시 초기 데이터 입력
    setInputData(Array.from({ length: inputCount }, (_, i) => 선수목록[i] || ''));

    if (apiData) {
      
      console.log('apiData')
      console.log(apiData)
      var table = document.getElementById('myTable');
      table.innerHTML = '';
      table.style.width = '90%'
  
      for (var i = 0; i < apiData.length; i++) {
        var rowData = apiData[i];
        var row = document.createElement('tr');
        row.style.display='flex';
  
        for (var j = 0; j < rowData.length; j++) {
          var cellData = rowData[j];
          var cell = document.createElement('td');
          cell.style.fontSize = '13px';
          cell.style.width='33%';
          cell.style.display='flex';
          cell.style.padding='20px';
  
          var draggableItems = cellData.map((player, mapIndex) => (
            <DraggableItem key={`item-${mapIndex}`} index={mapIndex} playerInfo={player} data_row={i} data_col={j}/>
          ));
  
          createRoot(cell).render(
            <section style={{display:'flex'}} >

            {draggableItems}


            </section>,
          );

          
          row.appendChild(cell);

          
        }
  
        table.appendChild(row);

        table.style.border = '1px solid black';
  
      }
    }
  }, [inputCount, apiData]);

  return (
    <div>
      <h1 style={{ color: 'green', fontWeight: 600 }}>🐸대전 스매시클럽 월례대회 팀 제작기🥎</h1>
      <div style={{ marginBottom: '5px' }}>참여자의 이름을 입력하세요. 추가 참여자는 추가로 입력해야 합니다.</div>

      <div style={{ marginBottom: '20px' }}>
        <button onClick={handleAddInput}>칸 추가</button>
        <button onClick={handleSubmit}>제출</button>
      </div>

      <div style={{ marginBottom: '20px' }}>
        {Array.from({ length: inputCount }, (_, i) => (
          <input
            key={`input-${i}`}
            style={{ width: '50px', marginRight: '20px' }}
            value={inputData[i]}
            onChange={(e) => handleInputChange(i, e.target.value)}
          />
        ))}
      </div>

      <h3 style={{ marginBottom: '20px' }}>결과창</h3>

      <table id="myTable">

      </table>
    </div>
  );
};

export default App;
