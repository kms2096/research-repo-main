(define (problem 01)
(:domain BANK)
(:objects SAM LOBBY GUN1 OWNER OUTSIDE VAULT-ROOM VAULT GOLD1 GOLD2)
(:INIT    (player sam) (character sam) (alive sam) (at sam lobby) (has sam gun1)
		  (character owner) (alive owner) (at owner outside)
		  (location vault-room) (connected vault-room lobby)
		  (closed vault) (at vault vault-room)
		  (location outside) (connected outside lobby)
		  (location lobby) (connected lobby vault-room) (connected lobby outside)
		  (thing gold1) (in gold1 vault)
		  (thing gold2) (in gold2 vault)
		  (gun gun1))
(:goal (AND (not (alive owner)) (open vault) (has owner gold1)))
)