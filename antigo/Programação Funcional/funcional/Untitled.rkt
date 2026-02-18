#lang racket


(require examples)

;;1
;; Número -> Número
;; Calcula o valor de x elevado ao quadrado.
(examples
 (check-equal? (quadrado 3) 9)
 (check-equal? (quadrado -2) 4))

(define (quadrado x)
  (* x x))

;; 2
;; InteiroPositivo -> Boolean
;;
;; Produz #t se uma pessoa com idade id é isento da
;; tarifa de transporte público, isto é, tem menos
;; que 18 anos ou 65 ou mais. Produz #f caso contrário.
(examples
 (check-equal? (isento-tarifa? 17) #t)
 (check-equal? (isento-tarifa? 18) #t)
 (check-equal? (isento-tarifa? 50) #f)
 (check-equal? (isento-tarifa? 65) #t)
 (check-equal? (isento-tarifa? 70) #t))

(define (isento-tarifa? id)
  (define idoso (or (= id 65) (> id 65)))
  (define jovem (or (= id 18) (< id 18)))
  (if (or jovem idoso) #t #f))


;; 3
;; String InteiroPositivo -> String
;; Produz uma string composta pela string original com o pósfixo de n pontos de exclamação.

(examples
 (check-equal? (gera-string "abacate" 0) "abacate")
 (check-equal? (gera-string "abacate" 3) "abacate!!!")
 (check-equal? (gera-string "abacate" 1) "abacate!"))

(define (gera-string frase n)
  (define exclamacao (make-string n #\!))
  (string-append frase exclamacao))

;; 4
;; NumeroPositivo -> NumeroPositivo
;; Retorna um valor baseado na taxa de correção num período de 2 anos (24 meses). A taxa de correção varia conforme o valor aplicado:
;; - Até R$ 2.000,00 -> taxa de 10%
;; - Entre 2.000,00 e 5.000,00 -> taxa de 12%
;; - Acima de R$ 5.000,00 -> taxa de 13%

(examples
 (check-equal? (calcula-correcao 2000) 2240.0)
 (check-equal? (calcula-correcao 1999) 2198.9)
 (check-equal? (calcula-correcao 4562) 5109.44)
 (check-equal? (calcula-correcao 5000) 5600.0)
 (check-equal? (calcula-correcao 7200) 8136.0))

(define (calcula-correcao valor)
  (cond
    [(< valor 2000) (+ (* valor 0.1) valor)]
    [ (> valor 5000) (+ (* valor 0.13) valor)]
    [else (+ (* valor 0.12) valor)]))


;; 5
;; Análise
;; Determinar uma direção oposta a que foi inserida pelo usuário
;; Determinar uma direção que está perpendicular (no sentido horário) da direção inserida
;; Determinar uma direção que está perpendicular (no sentido anti-horário) da direção inserida

;; Tipos de dados
;; Direção é um dos valores "norte", "sul", "leste" e "oeste"
;;       N
;;       |
;;   O -   - L
;;       |
;;       S

;; Direção -> Direção
;; Retorna a direção oposta

(examples
 (check-equal? (bussula-oposta "norte") "sul")
 (check-equal? (bussula-oposta "sul") "norte")
 (check-equal? (bussula-oposta "oeste") "leste")
 (check-equal? (bussula-oposta "leste") "oeste"))


(define (bussula-oposta ponto)
  (cond
    [(equal? ponto "norte") "sul"]
    [(equal? ponto "sul") "norte"]
    [(equal? ponto "oeste") "leste"]
    [(equal? ponto "leste") "oeste"]))

;; Direção -> Direção
;; Retorna a direção perpendicular no sentido horário

(examples
 (check-equal? (bussula-oposta-90-h "norte") "leste")
 (check-equal? (bussula-oposta-90-h "sul") "oeste")
 (check-equal? (bussula-oposta-90-h "oeste") "norte")
 (check-equal? (bussula-oposta-90-h "leste") "sul"))


(define (bussula-oposta-90-h ponto)
  (cond
    [(equal? ponto "norte") "leste"]
    [(equal? ponto "sul") "oeste"]
    [(equal? ponto "oeste") "norte"]
    [(equal? ponto "leste") "sul"]))


;; Direção -> Direção
;; Retorna a direção perpendicular no sentido anti-horário

(examples
 (check-equal? (bussula-oposta-90-ah "norte") "oeste")
 (check-equal? (bussula-oposta-90-ah "sul") "leste")
 (check-equal? (bussula-oposta-90-ah "oeste") "sul")
 (check-equal? (bussula-oposta-90-ah "leste") "norte"))


(define (bussula-oposta-90-ah ponto)
  (define cardeal (bussula-oposta ponto))
  (bussula-oposta-90-h cardeal))


;; 6
;; Análise
;; Determinar se uma data passada é a última do ano
;; Determinar se, ao se passar duas datas, deve retornar #t se a primeira vem antes da segunda

;; Tipos de dados
;; Data é um dado composto por dia, mês e ano, na ordem dia/mês/ano e são numeros positivos
;; dia - número de 1 a 31
;; mes - número de 1 a 12
;; ano - número de 0 a infinito

;; dia mes ano -> boolean

(examples
 (check-equal? (ultimo-dia 31 12 2023) #t)
 (check-equal? (ultimo-dia 31 12 2022) #t)
 (check-equal? (ultimo-dia 30 12 2023) #f)
 (check-equal? (ultimo-dia 31 01 2023) #f))

(define (ultimo-dia dia mes ano)
  (cond
    [(and (= mes 12) (= dia 31)) #t]
    [else #f]))

;; Data Data -> booleano

(examples
 (check-equal? (e-antes? 31 12 2023 02 01 2024) #t)
 (check-equal? (e-antes? 01 12 2024 01 12 2023) #f)
 (check-equal? (e-antes? 30 12 2023 1 4 2023) #f)
 (check-equal? (e-antes? 30 12 2023 30 12 2023) #f)
 (check-equal? (e-antes? 31 01 2023 31 12 2024) #t))

(define (e-antes? dia0 mes0 ano0 dia1 mes1 ano1)
  (cond
    [(< ano0 ano1) #t]
    [(< mes0 mes1) #t]
    [(< dia0 dia1) #t]
    [else #f]
    )
 )

;; 7
(struct retangulo (largura altura) #:transparent)
;; Representa um retângulo
;; largura: natural - largura do retângulo
;; altura: natural - altura do retângulo

(struct circulo (raio) #:transparent)
;; Representa um círculo
;; raio: natural - raio do círulo

;; Figura é um dos valores
;; - (retangulo natural natural)
;; - (ciculo natural)

(define PI 3.14)

;;Figura -> Real
;; Calcula a área da gfigura

(examples
  (check-= (area (retangulo 3.0 4.0)) 12.0 0.0)
  (check-= (area (circulo 2.0)) 12.56 0.0))

(define (area figura)
  (cond
[(retangulo? figura) (* (retangulo-altura figura) (retangulo-largura figura))]
[(circulo? figura) (* PI (sqr (circulo-raio figura)))]))


;; Figura -> Boolean
;;
;; Produz #t se a figura a cabe dentro da figura b, #f caso contrário.
;;
;; A seguinte tabela mostra as condições para a figura a caber
;; dentro da figura b. da é a diagonal da figura a se a é um retângulo.
;;
;; fig a \ fig b     |   (retangulo lb ab)      | (circulo rb)
;; ------------------|--------------------------|---------------
;; (retangulo la aa) |  la <= lb e aa <= ab     |  da <= 2 * rb
;; (circulo ra)      |  2*ra <= lb e 2*ra <= ab |  ra <= rb

(examples
  ; retangulo x retangulo
  (check-equal? (figura-cabe? (retangulo 5 18)
                              (retangulo 10 20)) #t)
  (check-equal? (figura-cabe? (retangulo 10 20)
                              (retangulo 10 20)) #t)
  (check-equal? (figura-cabe? (retangulo 11 20) ; largura não cabe
                              (retangulo 10 20)) #f)
  (check-equal? (figura-cabe? (retangulo 10 21) ; altura não cabe
                              (retangulo 10 20)) #f)
  ; retangulo (diagonal 5) x circulo
  (check-equal? (figura-cabe? (retangulo 3 4)
                              (circulo 3)) #t)
  (check-equal? (figura-cabe? (retangulo 3 4)
                              (circulo 2.5)) #t)
  (check-equal? (figura-cabe? (retangulo 3 4)
                              (circulo 2.4)) #f)
  ; circulo x retangulo
  (check-equal? (figura-cabe? (circulo 2)
                              (retangulo 4 4)) #t)
  (check-equal? (figura-cabe? (circulo 2)
                              (retangulo 4 4)) #t)
  (check-equal? (figura-cabe? (circulo 2)
                              (retangulo 3 4)) #f) ; não cabe na largura
  (check-equal? (figura-cabe? (circulo 2)
                              (retangulo 4 3)) #f) ; não cabe na altura
  ; circulo x circulo
  (check-equal? (figura-cabe? (circulo 2)
                              (circulo 3)) #t)
  (check-equal? (figura-cabe? (circulo 3)
                              (circulo 3)) #t)
  (check-equal? (figura-cabe? (circulo 4)
                              (circulo 3)) #f))

(define (figura-cabe? a b)
  (cond
    [(and (retangulo? a) (retangulo? b))
     (and (<= (retangulo-largura a)
              (retangulo-largura b))
          (<= (retangulo-altura a)
              (retangulo-altura b)))]
    [(and (retangulo? a) (circulo? b))
     (define diagonal (sqrt (+ (sqr (retangulo-largura a))
                         (sqr (retangulo-altura a)))))
     (<= diagonal (* 2 (circulo-raio b)))]
    [(and (circulo? a) (retangulo? b))
     (define diagonal (* 2 (circulo-raio a)))
     (and (<= diagonal (retangulo-largura b))
          (<= diagonal (retangulo-altura b)))]
    [(and (circulo? a) (circulo? b))
     (<= (circulo-raio a) (circulo-raio b))]))

;; 8
;; Análise
;; Bandeira é um dos valores
;; "verde"
;; "amarela"
;; "vermelha1"
;; "vermelha2"

;;Tipos de dados
;; Bandeiras:
;; Verde - acréscimo de R$ 0/Kwh
;; Amarela - acréscimo de R$ 0,01874/Kwh
;; Vermelha1 - acréscimo de R$ 0,03971/Kwh
;; Vermelha2 - acréscimo de R$ 0,09492/Kwh

(define tarifa-basica 0.888340)

;; Numero Bandeira -> Numero
(examples
 (check-equal? (consumo 10 "verde") 8.8834)
 (check-equal? (consumo 10 "amarela") 9.0708)
 (check-equal? (consumo 10 "vermelha1") 9.2805)
 (check-equal? (consumo 10 "vermelha2") 9.8326))

(define (consumo uso bandeira)
  (define (valor-ajustado tarifa) (+ tarifa-basica tarifa))
  (cond
    [(equal? bandeira "verde") (* (valor-ajustado 0) uso)]
    [(equal? bandeira "amarela") (* (valor-ajustado 0.01874) uso)]
    [(equal? bandeira "vermelha1") (* (valor-ajustado 0.03971) uso)]
    [(equal? bandeira "vermelha2") (* (valor-ajustado 0.09492) uso)]))

;; 9

