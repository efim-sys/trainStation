package main

import (
	"fmt"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
    var flag = false
    var i uint64
    var people uint64
    upd := make(chan bool)
    gin.SetMode(gin.ReleaseMode)
    server := gin.Default()
    server.Use(cors.Default())

    server.GET("/people", func(ctx *gin.Context) {
        flag = true

        fmt.Println("Got request.")

        ctx.Writer.Header().Set("Content-Type", "text/event-stream")
        ctx.Writer.Header().Set("Cache-Control", "no-cache")
        ctx.Writer.Flush()
        
        for {
            select {
            case <-upd:
                ctx.Writer.Write([]byte(fmt.Sprintf("id: %d\n", i)))
                i++
                ctx.Writer.Write([]byte("event: people\n"))
                ctx.Writer.Write([]byte(fmt.Sprintf("data: %d\n", people)))
                ctx.Writer.Write([]byte("\n"))
                ctx.Writer.Flush()
                // fmt.Println("Sent.")

            }
        }
    })
    go server.Run(":3000")
    for {
        if flag {
            fmt.Print("Enter amount of people: ")
            fmt.Scanln(&people)
            upd <- true
        }
    }
}