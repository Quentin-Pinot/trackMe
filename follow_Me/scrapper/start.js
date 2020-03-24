var express = require("express");
const { Client } = require("pg");
const connectionString = "postgres://postgres:admin@localhost:4321/followMe";

const client = new Client({
  connectionString: connectionString
});
client.connect();

var app = express();

// J'enleve pour voir si je peux pas faire sans
// app.set("port", process.env.PORT || 4000);

app.get("/name", callName);

function callName(req, res) {
  var spawn = require("child_process").spawn;

  client.query(
    "INSERT INTO item(id_item, title, prix, url, id_user) VALUES(1, 'titreTest', 100, 'https://www.amazon.fr/LG-Smart-Dolby-Vision-OLED55C9PLA/dp/B07QNS1LVK/ref=sr_1_3?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=24Y19O45XVKX6&keywords=tv+oled+55+pouces+4k&qid=1584723700&sprefix=tv%2Caps%2C153&sr=8-3', 1)"
  );

  var process = spawn("python", ["./main.py"]);

  // Takes stdout data from script which executed
  // with arguments and send this data to res object
  process.stdout.on("data", function(data) {
    console.log(data.toString());
    res.send(data.toString());
  });
}

// Creates a server which runs on port 3000 and
// can be accessed through localhost:3000
app.listen(4000, function() {
  console.log("server running on port 4000");
});
