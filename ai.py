# ai.py
import random
import copy
from settings import *

class AI:
    def __init__(self, player_id):
        self.id = player_id

    def get_best_move(self, board, p1, p2):
        """Root of the Minimax algorithm."""
        # Determine who is the AI player object
        ai_player = p2 if self.id == 2 else p1
        opp_player = p1 if self.id == 2 else p2

        # print("AI Thinking...") # Uncomment for debug
        
        # 1. Get valid moves from the current state
        possible_moves = self.get_all_moves(board, ai_player, opp_player)
        
        best_score = -float('inf')
        best_move = None
        
        alpha = -float('inf')
        beta = float('inf')

        for move in possible_moves:
            # 2. Create a simulation board for the recursive steps
            sim_board = board.clone()
            sim_ai = self.clone_player(ai_player)
            sim_opp = self.clone_player(opp_player)
            
            # 3. Apply the move to the simulation
            self.apply_move(sim_board, sim_ai, sim_opp, move)
            
            # 4. Call Minimax
            score = self.minimax(sim_board, AI_DEPTH - 1, alpha, beta, False, sim_ai, sim_opp)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        
        # Fallback if no move found
        if best_move is None and possible_moves:
            best_move = random.choice(possible_moves)
                
        return best_move

    def minimax(self, board, depth, alpha, beta, is_maximizing, ai_player, opp_player):
        # 1. Base Case: Check for winner or depth limit
        ai_dist = board.get_shortest_path_len(ai_player.pos, ai_player.goal_row)
        opp_dist = board.get_shortest_path_len(opp_player.pos, opp_player.goal_row)

        if ai_dist == -1: ai_dist = INF
        if opp_dist == -1: opp_dist = INF

        if ai_dist == 0: return INF 
        if opp_dist == 0: return -INF 
        
        if depth == 0:
            return opp_dist - ai_dist

        if is_maximizing:
            max_eval = -float('inf')
            moves = self.get_all_moves(board, ai_player, opp_player)
            for move in moves:
                sim_board = board.clone()
                sim_ai = self.clone_player(ai_player)
                sim_opp = self.clone_player(opp_player)
                
                self.apply_move(sim_board, sim_ai, sim_opp, move)
                
                eval = self.minimax(sim_board, depth - 1, alpha, beta, False, sim_ai, sim_opp)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = float('inf')
            moves = self.get_all_moves(board, opp_player, ai_player)
            for move in moves:
                sim_board = board.clone()
                sim_ai = self.clone_player(ai_player)
                sim_opp = self.clone_player(opp_player)
                
                self.apply_move(sim_board, opp_player, ai_player, move)
                
                eval = self.minimax(sim_board, depth - 1, alpha, beta, True, sim_ai, sim_opp)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval

    def get_all_moves(self, board, active_player, waiting_player):
        moves = []
        
        # 1. Pawn Moves
        pawn_moves = board.get_valid_moves(active_player, waiting_player)
        for pm in pawn_moves:
            moves.append(('move', pm))
            
        # 2. Wall Moves
        if active_player.walls_remaining > 0:
            focus_points = [active_player.pos, waiting_player.pos]
            checked = set()
            
            # Unpacking tuple (x, y) into fx, fy directly
            for fx, fy in focus_points:
                # Search range: 1 cell around players
                # FIX: Use fx and fy directly (they are integers), do not use fx[0]
                for cx in range(fx - 1, fx + 2):
                    for cy in range(fy - 1, fy + 2):
                        
                        if 0 <= cx < BOARD_SIZE - 1 and 0 <= cy < BOARD_SIZE - 1:
                            if (cx, cy) in checked: continue
                            checked.add((cx, cy))
                            
                            # Check Horizontal
                            # We use a clone to check validity without ruining the main board
                            test_board_h = board.clone() 
                            if test_board_h.place_wall(cx, cy, 'H', active_player, waiting_player):
                                moves.append(('wall', (cx, cy), 'H'))
                            
                            # Check Vertical
                            test_board_v = board.clone()
                            if test_board_v.place_wall(cx, cy, 'V', active_player, waiting_player):
                                moves.append(('wall', (cx, cy), 'V'))

        random.shuffle(moves)
        return moves

    def apply_move(self, board, active_player, waiting_player, move):
        type, data = move[0], move[1]
        if type == 'move':
            active_player.pos = data
        elif type == 'wall':
            coords = data
            orientation = move[2]
            board.place_wall(coords[0], coords[1], orientation, active_player, waiting_player)
            active_player.walls_remaining -= 1

    def clone_player(self, player):
        from player import Player
        p = Player(player.pos, player.color, player.goal_row, player.id)
        p.walls_remaining = player.walls_remaining
        return p