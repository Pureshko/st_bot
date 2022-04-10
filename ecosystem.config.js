module.exports = {
  apps : [{
    name   : "st_bot",
    script : "./st_bot.py",
    watch: true,
    env: {
       TBOTTOKEN: "5268370640:AAGLuB_lWaM70mS4bOGb8YHDP4q60qp-Atw",
       DBPATH: "class.db"
    }
  }]
};
