const { fork } = require("child_process");
const find = require("find-process");
const ps = require("ps-node");

process.on("message", (message) => {
  if (message.type === "SIGNAL") {
    console.log("I'm collector Received signal from the clock");

    //get variable
    let variable = message.variable;

    ps.lookup({ pid: message.variable.pid }, function (err, resultList) {
      if (err) {
        throw new Error(err);
      }
      variable = resultList[0];
      console.log("ma variable est : ", variable);
      variable.send({ type: "GET_CAPTEUR", process });
      variable.on("message", (message) => {
        if (message.type === "CAPTEUR") {
          const capteurs = message.capteur;
          for (let i = 0; i < capteurs.length; i++) {
            capteurs[i].send({ type: "GIVE ME VALUE", process });
          }
        }
      });
    });

    //variable.send({ type: "GET_CAPTEUR", process });
  }

  if (message.type === "TEMPERATURE_MEASUREMENT") {
    console.log("I'm collector Received signal from the capteur");
    console.log(message.temperature);
  }
});
