//import fetch from 'node-fetch';

let express = require('express');
let app = express();

//Socket Conection
let server = require('http').Server(app);
let io = require('socket.io')(server);

//Middleware
const ejs = require('ejs');
app.use(express.static('public')); //specify location of static assests
app.set('views', __dirname + '/views'); //specify location of templates
app.set('view engine', 'ejs'); //specify templating library

io.on('connection', function(socket){  

  io.emit('connection', {
    num_total_connections: io.engine.clientsCount
  }); 

  socket.on('meep', async function(data) {  
    const get_game_data_link = `http://127.0.0.1:8080/games/data/${data.game_name}`;
    const game_response = await fetch(get_game_data_link)
    const game_data = await game_response.json();
    //console.log("muy gae dataa",game_data)

    const get_scorecards_link = `http://127.0.0.1:8080/games/scorecards/${data.game_name}`;
    const scorecards_response = await fetch(get_scorecards_link)
    const scorecards_data = await scorecards_response.json();
    console.log("muy gae dataa",scorecards_data)
    
    console.log("the username im emitting is",data.username)

    io.to(data.game_name).emit('meep', {
      username:data.username,
      usernames_list: game_data["usernames_list"],
      scorecards_list: scorecards_data
    });

  }); 

  socket.on('disconnect', async function(data){
    console.log("someone has disconnected")

    console.log(socket.game_name)
    
    if (socket.game_name){
      const room = io.sockets.adapter.rooms.get(socket.game_name);
      if (room){
        io.to(socket.game_name).emit('goodbye', {
          num_game_connections: io.sockets.adapter.rooms.get(socket.game_name).size,
        });
      }
    }
  });

  socket.on('game_connection', async function(data) {  
    socket.join(data.game_name);

    socket.game_name = data.game_name;

    console.log('Socket game connection event:', data.username, io.sockets.adapter.rooms.get(data.game_name).size);

    const get_scorecards_link = `http://127.0.0.1:8080/games/scorecards/${data.game_name}`;
    const scorecards_response = await fetch(get_scorecards_link)
    const scorecards_data = await scorecards_response.json();

    //scorecards_data = JSON.parse(scorecards_data)
    // for (let i=0; i<scorecards_data.length; i++){
    //   for (const section in scorecards_data[i]["categories"]){
    //     if (scorecards_data[i]["categories"] != "rolls_remaining"){
    //       scorecards_data[i]["categories"][section] = JSON.stringify(scorecards_data[i]["categories"][section])
    //     }
    //     console.log(scorecards_data[i]["categories"][section])
    //   }
    // }

    console.log("Scorecards loaded:", scorecards_data);
    // for (const category in scorecards_data[1]["categories"]["upper"]){
    //   console.log(scorecards_data[1]["categories"]["upper"][category])
    // }
    //console.log("Emitting scorecards_list:", JSON.stringify(scorecards_data, null, 2));


    io.to(data.game_name).emit('game_connection', {
      username:data.username,
      num_game_connections: io.sockets.adapter.rooms.get(data.game_name).size,
      scorecards_list: scorecards_data
    });
    
  }); 

  socket.on('chat', function(data) {
    console.log('Socket chat event:', data);
    io.to(data.game_name).emit('chat', {
      username: data.username,
      message: data.message
    });
  });

  socket.on('valid_score_submitted', function(data) {
    console.log(`📢 Emitting valid_score_submitted to room: ${data.game_name}`);
    console.log('Socket valid score submitted event:', data);
    io.to(data.game_name).emit('valid_score_submitted', {
      event_username: data.event_username,
      score_info: data.score_info
    });
    
    const body = data.score_info;
    body["rolls_remaining"] = 3;
    body["username"] = data.event_username
    body["game_name"] = data.game_name
    for (const section in body){
      //console.log(section)
      if (section != "rolls_remaining"){
        for (const category in body[section]){
          // console.log(`${category}: ${body[section][category]}`);
          
          let bar_position = category.indexOf("|")
          let extracted_username = category.slice(bar_position)
          without_username = category.replace(extracted_username,"")
          
          //console.log(body[section][category])
          body[section][without_username] = body[section][category]; 
          //console.log(`${without_username}: ${body[section][without_username]}`);
          delete body[section][category];
        }
      }
    }
    console.log(body)



    //send post request for scorecard data
    async function send_scorecard(){
      
      const response = await fetch('http://127.0.0.1:8080/games/receive/scorecard', {
        method: 'post',
        body: JSON.stringify(body),
        headers: {'Content-Type': 'application/json'}
      });
      const data = await response;

      console.log(data);
    }

    send_scorecard()
  });
});

app.get('/games/:game_name/:username', async function(request, response) {
  let username = request.params.username;
  let game_name = request.params.game_name;
  // needs to be an async function to use fetch w await
  //testing

  // const body = {a: 1};
  // const response1 = await fetch('https://httpbin.org/post', {
  //   method: 'post',
  //   body: JSON.stringify(body),
  //   headers: {'Content-Type': 'application/json'}
  // }); 
  // const data = await response1.json();
  // console.log(data);

  //fetch request to python server to know which players are in the game, which columns to create , get request for game data
  const get_game_data_link = `http://127.0.0.1:8080/games/data/${game_name}`;
  const game_response = await fetch(get_game_data_link)
  const game_data = await game_response.json();
  console.log(game_data)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("index", {
    username: username,
    game_name: game_name,
    usernames_list: [username],
    //send another variable that is from a fetc hthat gets all the scorecards from the pyton server --> this allows the scorecards to be loaded every time the game is loaded
  });
});

//start the server
const port = process.env.PORT || 3000;
app.set('port', port); //let heroku pick the port if needed

server.listen(port, function() {
  console.log('Server started at http://localhost:'+port+'.')
});



