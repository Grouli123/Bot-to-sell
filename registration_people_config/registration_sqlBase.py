name_of_base = 'users'
createDatabase = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, DATETIME DEFAULT CURRENT_TIMESTAMP, phone varchar(50), city varchar(50), last_name varchar(50), firts_name varchar(50), middle_name varchar(50), birthday data, citizenRF varchar(50), user_id INTEGER, samozanatost varchar(50), agreeacc varchar(50), passport varchar(50), botchatname varchar(50), cityAgree varchar(50), actualOrder varchar(50), orderTake TEXT, orderDone TEXT, orderMiss TEXT, botChatId varchar(50), raiting INTEGER, orderDefect TEXT)'
insertIntoDatabase = "INSERT INTO users (phone, city, last_name, firts_name, middle_name, birthday, citizenRF, user_id, samozanatost, agreeacc, passport, botchatname, cityAgree, actualOrder, orderTake, orderDone, orderMiss, botChatId, raiting, orderDefect) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
# updateDatabase = "UPDATE users SET (phone, city, last_name, firts_name, middle_name, birthday, citizenRF, samozanatost, agreeacc, passport, botchatname, cityAgree, actualOrder, orderTake, orderDone, orderMiss, botChatId, raiting, user_id)"

updateDatabase = """
UPDATE users 
SET phone = ?, 
    city = ?, 
    last_name = ?, 
    firts_name = ?, 
    middle_name = ?, 
    birthday = ?, 
    citizenRF = ?, 
    samozanatost = ?, 
    agreeacc = ?, 
    passport = ?, 
    botchatname = ?, 
    cityAgree = ?, 
    actualOrder = ?, 
    orderTake = ?, 
    orderDone = ?, 
    orderMiss = ?, 
    botChatId = ?, 
    raiting = ?,
    orderDefect = ?
WHERE user_id = ?
"""
