library(toRvik)
library(RSQLite)

con <- dbConnect(RSQLite::SQLite()
    , dbname ="C:\\Users\\Tyler Dufrene\\Documents\\TylerDufrene\\Data Science\\sports_data\\sports_reference.db")

ratings <- data.frame(bart_ratings(202))

dbWriteTable(con, name="ncaab_toRvik_ratings",
    value = ratings, row.names = FALSE, overwrite=FALSE, append=TRUE
)

dbDisconnect(con)