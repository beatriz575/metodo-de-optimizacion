library(shiny)

# Función: Sustitución
resolver_sustitucion <- function(a1, b1, c1, a2, b2, c2) {
  # Despejar y de la primera ecuación
  if (b1 == 0) stop("No se puede aplicar sustitución si b1 = 0")
  despeje_y <- function(x) (c1 - a1 * x) / b1
  # Reemplazar en la segunda ecuación y resolver
  f <- function(x) a2 * x + b2 * despeje_y(x) - c2
  x_val <- uniroot(f, c(-1e3, 1e3))$root
  y_val <- despeje_y(x_val)
  return(c(x = round(x_val, 4), y = round(y_val, 4)))
}

# Función: Igualación
resolver_igualacion <- function(a1, b1, c1, a2, b2, c2) {
  # Despejar y de ambas ecuaciones
  if (b1 == 0 || b2 == 0) stop("No se puede aplicar igualación si b1 o b2 = 0")
  y1 <- function(x) (c1 - a1 * x) / b1
  y2 <- function(x) (c2 - a2 * x) / b2
  f <- function(x) y1(x) - y2(x)
  x_val <- uniroot(f, c(-1e3, 1e3))$root
  y_val <- y1(x_val)
  return(c(x = round(x_val, 4), y = round(y_val, 4)))
}

# Función: Reducción
resolver_reduccion <- function(a1, b1, c1, a2, b2, c2) {
  mat <- matrix(c(a1, b1, a2, b2), ncol = 2, byrow = TRUE)
  vec <- c(c1, c2)
  sol <- solve(mat, vec)
  return(c(x = round(sol[1], 4), y = round(sol[2], 4)))
}

# UI
ui <- fluidPage(
  titlePanel("🔢 Resolución de Sistemas de Ecuaciones Lineales"),
  
  sidebarLayout(
    sidebarPanel(
      numericInput("a1", "a₁ (coef. de x en Ecuación 1):", value = 1),
      numericInput("b1", "b₁ (coef. de y en Ecuación 1):", value = 1),
      numericInput("c1", "c₁ (resultado de Ecuación 1):", value = 1),
      numericInput("a2", "a₂ (coef. de x en Ecuación 2):", value = 1),
      numericInput("b2", "b₂ (coef. de y en Ecuación 2):", value = 1),
      numericInput("c2", "c₂ (resultado de Ecuación 2):", value = 1),
      selectInput("metodo", "Método de resolución:",
                  choices = c("Sustitución", "Igualación", "Reducción")),
      actionButton("resolver", "✅ Resolver")
    ),
    
    mainPanel(
      h4("📌 Resultado:"),
      verbatimTextOutput("resultado"),
      tags$br(),
      tags$p("Este programa resuelve sistemas de ecuaciones lineales con dos variables usando métodos algebraicos.")
    )
  )
)

# Servidor
server <- function(input, output) {
  observeEvent(input$resolver, {
    a1 <- input$a1; b1 <- input$b1; c1 <- input$c1
    a2 <- input$a2; b2 <- input$b2; c2 <- input$c2
    metodo <- input$metodo
    
    resultado <- tryCatch({
      if (metodo == "Sustitución") {
        res <- resolver_sustitucion(a1, b1, c1, a2, b2, c2)
      } else if (metodo == "Igualación") {
        res <- resolver_igualacion(a1, b1, c1, a2, b2, c2)
      } else {
        res <- resolver_reduccion(a1, b1, c1, a2, b2, c2)
      }
      paste0("✅ Solución encontrada:\n  x = ", res["x"], "\n  y = ", res["y"])
    }, error = function(e) {
      paste("❌ Error:", e$message)
    })
    
    output$resultado <- renderText({ resultado })
  })
}

shinyApp(ui = ui, server = server)


   