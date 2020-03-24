const { Pool } = require("pg");
var express = require("express"),
  session = require("express-session"),
  pgSession = require("connect-pg-simple")(session),
  bodyParser = require("body-parser");

let d = new Date();
let date = `${d.getDay()}-${d.getMonth()}-${d.getYear()} ${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}: `;

const {
  PORT = 8080,
  PGHOST = "localhost",
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

  res.sendfile(__dirname + "\\index.html");
});

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

  // req.session.use;
});

app.get("/register", (req, res) => {
  res.sendfile(__dirname + "\\register.html");
});

app.post("/login", redirectHome, (req, res) => {
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

app.post("/register", redirectHome, (req, res) => {
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

app.post("/logout", redirectLogin, (req, res) => {
  console.log(date + "Logout of userId '" + req.session.userId + "'");

  req.session.destroy(err => {
    if (err) {
      console.log(date + err);
      return res.redirect("/");
    }
    else {
      res.clearCookie(SESS_NAME);

      return res.redirect("/");
    }
  });
});

/* On utilise les sessions */
app.listen(PORT, () =>
  console.log(date + "Serveur is listening in http://localhost:" + PORT)
);

// todo : Commenter un max