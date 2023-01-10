const { fork } = require("child_process");

const collector = [];
const capteur = [];
const controller = [];

process.on("message", (message) => {
  if (message.type === "NEW_COLLECTOR") {
    collector.push(message.pid);
  }

  if (message.type === "NEW_CONTROLLER") {
    controller.push(message.pid);
  }

  if (message.type === "NEW_CAPTEUR") {
    capteur.push(message.pid);
  }

  if (message.type === "GET_CAPTEUR") {
    process.send({ type: "CAPTEUR", capteur });
  }
});
