package main

import (
	"database/sql"
	"fmt"
	"github.com/jasonlvhit/gocron"
	_ "github.com/lib/pq"
	"time"
)

const (
	host     = "db"
	port     = 5432
	user     = "myturf"
	password = "myturf_pass"
	dbname   = "myturf_db"
)
// fmt.Println("helloooooooooooooo")

func main(){


	// ###########################db connection #################################

	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+"password=%s dbname=%s sslmode=disable",host, port, user, password, dbname)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}
	fmt.Println("Successfully connected!7777777777777")
	
	// ###########################db connection end#################################

	// ###########################crone job #######################################

	gocron.Every(2).Second().Do(updateTournamentStatus, db)
	<-gocron.Start()

	// ###########################crone job end#######################################
	
	
}

	func updateTournamentStatus(db *sql.DB){

		
		fetch_tournament_rows,err:= db.Query(`SELECT id,extract(epoch from start_time at time zone 'UTC')::int as start_time , extract(epoch from end_time at time zone 'UTC')::int as end_time FROM "User_tournamentmodel" WHERE cron=1 `)
		if err != nil {
			
			fmt.Println("error 1 :",err)
		}
		
		defer fetch_tournament_rows.Close()
		
		for fetch_tournament_rows.Next() {
			var tournament_id int
			var start_time int64
			var end_time int64
			
			err = fetch_tournament_rows.Scan(&tournament_id, &start_time , &end_time)
			if err != nil {
				// handle this error
				fmt.Println("error 2 :",err)
			}
			
			
			upadateCrone(0, db, tournament_id)
			
			//##############################update status start
			// t:=time.Now()
			// fmt.Println("timeeeeeeeeeeeeeeeeeeee check ::",start_time<time.Now())
			
				t:=time.Now()
			
				start_time_converted := time.Unix(start_time, 0)
				end_time_converted := time.Unix(end_time, 0)
				// fmt.Println(start_time_converted," :  start_time_converted")
				// fmt.Println(t," :  time now" )
			  
				
					// t := time.Now()
					if t.After(start_time_converted) && t.Before(end_time_converted) {
						fmt.Println("started................tournament")
						upadateCrone(1, db, tournament_id)
						updateStatus("Started", db, tournament_id)
						}else if t.After(end_time_converted){
							fmt.Println("Completed................tournament")
							updateStatus("Completed", db, tournament_id)
							upadateCrone(0, db, tournament_id)
						}else{
							upadateCrone(1, db, tournament_id)
						}
					
				
				
				
			
			//##############################update cron end

			



			fmt.Println(tournament_id, start_time, end_time)

		  }
		  // get any error encountered during iteration
		  err = fetch_tournament_rows.Err()
		  if err != nil {
			fmt.Println("error 3 :",err)
		  }


	}
	func upadateCrone(cron int, db  *sql.DB, tournament_id int){
		//##############################update cron start 
		update_cron := `
		UPDATE "User_tournamentmodel"
		set cron = $1 WHERE id = $2`

		_, err_update_cron := db.Exec(update_cron,cron,tournament_id)
		if err_update_cron != nil {
			fmt.Println("update_cron :", err_update_cron)
		}
		//##############################update cron end
	}

func updateStatus(status string, db *sql.DB, tournament_id int){
	update_cron := `
		UPDATE "User_tournamentmodel"
		set status = $1 WHERE id = $2`

		_, err_update_cron := db.Exec(update_cron,status,tournament_id)
		if err_update_cron != nil {
			fmt.Println("update_cron :", err_update_cron)
		}
}