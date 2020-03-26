const { Pool } = require("pg");
var express = require("express"),
  session = require("express-session"),
  pgSession = require("connect-pg-simple")(session),
  bodyParser = require("body-parser");

let d = new Date();
let date = `${d.getDay()}-${d.getMonth()}-${d.getYear()} ${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}: `;

const {
  PORT = 8080,
  PGHOST = "127.0.0.1",
  PGUSER = "postgres",
  PGDATABASE = "followMe",
  PGPASSWORD = "admin",
  PGPORT = "4321",
  NODE_ENV = "development",
  SESS_NAME = "sid",
  SESS_SECRET = "raboule_le_fric_amazon",
  SESS_LIFETIME = 24 * 60 * 60 * 1000 // 24h
} = process.env;

const pool = new Pool({
  user: PGUSER,
  host: PGHOST,
  database: PGDATABASE,
  password: PGPASSWORD,
  port: PGPORT
});

const IN_PROD = NODE_ENV === "production";

var app = express();

app.use(
  bodyParser.urlencoded({
    extended: true
  })
);

app.use(
  session({
    name: SESS_NAME,
    store: new pgSession({
      pool: pool,
      tableName: "sessionUser"
    }),
    resave: false,
    saveUninitialized: false,
    secret: SESS_SECRET,
    cookie: {
      maxAge: SESS_LIFETIME,
      sameSite: true,
      secure: IN_PROD
    }
  })
);

const redirectLogin = (req, res, next) => {
  if (!req.session.userId) {
    console.log(date + "Redirected login page")

    res.redirect("/login");
  } else {
    next();
  }
};

app.get("/", redirectLogin, (req, res) => {
  console.log(date + "Home page")

  const { userId } = req.session;

  pool.query("SELECT * FROM utilisateur WHERE id_user = " + userId, (err, resp) => {
    if (err) {
      console.log(date + "Error bdd -> " + err.stack)
    }
    else {
      if (resp.rows[0]) {
        res.locals.user = resp.rows[0];

        const user = res.locals.user;

        console.log(date + "User online -> '" + user.pseudo + "'");

        pool.query("SELECT * FROM item WHERE id_user = " + user.id_user, (err, resp) => {
          if (err) {
            console.log(date + "Error bdd -> " + err.stack);
          }
          else {
            if (resp.rows[0]) {
              console.log(date + "Affichage des items linked à '" + user.pseudo + "'")
              const itemsLinked = resp.rows;
              res.render('index.ejs', { UserOnline: user, Items: itemsLinked });
            }
            else {
              res.render('index.ejs', { UserOnline: user });
            }
          }
        });
      }
    }
  });
});

app.post("/", (req, res) => {
  const { url_To_Track } = req.body;

  pool.query("SELECT COUNT(id_item) FROM item", (err, resp) => {
    if (err) {
      console.log(date + "Error bdd -> " + err.stack);
    }
    else {
      if (resp.rows[0]) {
        const id_item = parseInt(Object.values(resp.rows[0])) + 1

        pool.query("INSERT INTO item(id_item, url, date_add, id_user)" +
          "VALUES(" + id_item + ", '" + url_To_Track + "',  CURRENT_DATE, " + req.session.userId + ");", (err, respo) => {
            if (err) {
              console.log(date + "Error bdd -> " + err.stack)
              // todo : en cas d'erreur le notifier au user avec un message et redirect la page au meme endroit
            }
            else {
              console.log(date + "Ajout de l'item '" + id_item + "' a la bdd");

              console.log(date + "lancement du script python pour scrapper");
              const { spawn } = require("child_process");
              const child = spawn("python", ["./scrapper/main.py ", req.session.userId, id_item]);

              child.stdout.on('data', (data) => {
                console.log(date + data.toString())
              });

              child.on('exit', () => {
                console.log(date + "Fin du script python")
                res.redirect("/")
              });
            }
          })
      }
    }
  })
})


const redirectHome = (req, res, next) => {
  if (req.session.userId) {
    console.log(date + "Redirected home page")

    res.redirect("/");
  } else {
    next();
  }
};

app.get("/login", redirectHome, (req, res) => {
  console.log(date + "Login page")

  res.sendfile(__dirname + "\\login.html");
});

app.post("/login", (req, res) => {
  const { pseudo, password } = req.body;

  console.log(
    date + "Tentative de connection de '" + pseudo + "' avec un mdp '" + password + "'"
  );

  if (pseudo && password) {
    // todo : Verification de la sophistication du mdp
    // todo : HASH the password 
    pool.query(
      "SELECT id_user, pseudo, mdp FROM utilisateur WHERE pseudo = " +
      "'" + pseudo +
      "'" + " AND mdp = " + "'" + password + "'",
      (err, resp) => {
        if (err) {
          console.log(date + "Error bdd -> ");
          console.log(date + err.stack);
        }
        else {
          if (resp.rows[0]) {
            if (Object.values(resp.rows[0])[1] == pseudo && Object.values(resp.rows[0])[2] == password) {
              console.log(date + "Connexion effectue de '" + Object.values(resp.rows[0])[1] + "'");

              req.session.userId = Object.values(resp.rows[0])[0];
              res.redirect("/");
            }
          }
          else {
            console.log(date + "User not find");

            res.redirect("/");
          }
        }
      }
    );
  }
});


app.get("/register", redirectLogin, (req, res) => {
  res.sendfile(__dirname + "\\register.html");
});

app.post("/register", (req, res) => {
  const { firstName, lastName, pseudo, password, email } = req.body;

  if (firstName && lastName && pseudo && password && email) { // todo : VALIDATION des champs
    pool.query(
      "SELECT pseudo, mail FROM utilisateur WHERE pseudo = " +
      "'" + pseudo +
      "'" + " AND mail = " + "'" + email + "'",
      (err, resp) => {
        if (err) {
          console.log(date + "Error bdd -> ");
          console.log(date + err.stack);
        }
        else {
          if (resp.rows[0]) {
            if (Object.values(resp.rows[0])[0] == pseudo && Object.values(resp.rows[0])[1] == email) {
              console.log(date + "User '" + Object.values(resp.rows[0])[0] + "' with mail '" + Object.values(resp.rows[0])[1] + "' already exist");

              res.redirect("/");
            }
          }
          else {
            pool.query("SELECT MAX(id_user)+1 FROM utilisateur",
              (err, respo) => {
                if (err) {
                  console.log(date + "Error bdd -> ");
                  console.log(date + err.stack);
                }
                else {
                  pool.query(
                    "INSERT INTO utilisateur(id_user, pseudo, mdp, mail, prenom, nom) " +
                    "VALUES(" + Object.values(respo.rows[0])[0] + ", '" +
                    pseudo + "', '" + password + "', '" + email + "', '" + firstName + "', '" + lastName + "');",
                    (err) => {
                      if (err) {
                        console.log(date + "Error bdd -> "); console.log(date + err.stack);
                      }
                      else {
                        console.log(date + 'User ' + pseudo + ' has been created');

                        req.session.userId = Object.values(respo.rows[0])[0];

                        res.redirect("/");
                      }
                    });
                }
              });
          }
        }
      });
  }
});

app.post("/logout", (req, res) => {
  console.log(date + "Logout of userId '" + req.session.userId + "'");

  req.session.destroy(err => {
    if (err) {
      console.log(date + "Error of logout -> " + err);
      return res.redirect("/");
    }
    else {
      res.clearCookie(SESS_NAME);

      return res.redirect("/");
    }
  });
});

// En cas d'url incorrect on redirect a la page d'acceuil
app.use(function (req, res, next) {
  res.redirect('/');
})

// Lancement du serveur
app.listen(PORT, () =>
  console.log(date + "Serveur is listening in http://localhost:" + PORT)
);

// todo : Commenter un max