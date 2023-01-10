const { fork } = require("child_process");

process.on("message", (message) => {
  if (message.type === "GIVE ME VALUE") {
    console.log("I'm capteur");

    // une probabilité d'envoyé la bonne valeur
    // une probabilité qui s'envoie pas du tout de valeur
    // une probabilité qui envoie la mauvaise valeur

    const temperature = Math.floor(Math.random() * 100);
    message.process.send({
      type: "TEMPERATURE_MEASUREMENT",
      temperature,
    });
  }
});
