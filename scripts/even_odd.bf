;====== repl ======;
https://replit(dot)com/@JoeyLent/EvenOdd(dash)checker

;====== note ======;
check the 'min' for the minified version


;==== thestack ====;
| 1  | 0  | 0  | x  |    |
|Loop|Even|Odd |num |    |
               |chr table|


;====== init ======;

; set this to a value between 0 and 255
>>>++++

; set true and false values
<<<+


;===== checks =====;

[
  ; check if subtracting one returns zero (odd)
  >>>-
  [
    ; check if subtracting one returns zero (even)
    -
    [
      <
    ]
    <
  ]
  <
]


;===== result =====;

; init "char table"
; used to make printing text much easier
++++++++++[
  100 >++++++++++
  110 >+++++++++++
  <<-
]

; move left and check if cell is not zero (loop cell; even)
<
[
  ; move to "char table"
  >>

  ; print even
  e +.
  v >++++++++.
  e <.
  n >--------. 

  ; set loop to 0 to skip odd checks
  <<<-->
]

; check if cell is not zero (odd)
; the cell will be 0 when adding a 1 if the previous loop ran
;   effectively skipping the loop
<+
[
  ; move to "char table"
  >>>

  ;print odd
  o >+.
  d <.
  d .

  ; go to start and set to 0 to exit loop
  <<<--
]