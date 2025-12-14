import random
from settings import *

class AI:
    def __init__(self, player_id):
        self.id = player_id

    def get_best_move(self, board, p1, p2):
        ai_player = p2 if self.id == 2 else p1
        opp_player = p1 if self.id == 2 else p2

        # 1. Get all possible moves
        possible_moves = self.get_all_moves(board, ai_player, opp_player)
        
        best_score = -float('inf')
        best_move = None
        
        alpha = -float('inf')
        beta = float('inf')

        # To prevent the AI from being too predictable, we shuffle
        random.shuffle(possible_moves)

        for move in possible_moves:
            sim_board = board.clone()
            sim_ai = self.clone_player(ai_player)
            sim_opp = self.clone_player(opp_player)
            
            self.apply_move(sim_board, sim_ai, sim_opp, move)
            
            # Using Depth 2 (Current move + Opponent response)
            # Increase AI_DEPTH in settings.py to 3 if your computer is fast
            score = self.minimax(sim_board, AI_DEPTH - 1, alpha, beta, False, sim_ai, sim_opp)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
            if beta <= alpha:
                break
                
        return best_move

    def evaluate_state(self, board, ai_p, opp_p):
        """
        The Brain of the AI. 
        Higher score = Better for AI.
        """
        ai_dist = board.get_shortest_path_len(ai_p.pos, ai_p.goal_row)
        opp_dist = board.get_shortest_path_len(opp_p.pos, opp_p.goal_row)

        # Handle blocked paths (shouldn't happen with Quoridor rules, but safe-check)
        if ai_dist == -1: ai_dist = 50 
        if opp_dist == -1: opp_dist = 50

        # Victory / Defeat conditions
        if ai_dist == 0: return 1000
        if opp_dist == 0: return -1000

        # --- HEURISTIC CALCULATION ---
        # 1. Distance difference: We want a high gap (AI closer, Player further)
        # We multiply Opponent distance by 1.2 to make AI more aggressive in blocking
        score = (opp_dist * 1.5) - (ai_dist)

        # 2. Wall count: AI should value having more walls than the opponent
        score += (ai_p.walls_remaining - opp_p.walls_remaining) * 0.5

        return score

    def minimax(self, board, depth, alpha, beta, is_maximizing, ai_player, opp_player):
        if depth == 0:
            return self.evaluate_state(board, ai_player, opp_player)

        # Check for terminal states
        ai_dist = board.get_shortest_path_len(ai_player.pos, ai_player.goal_row)
        opp_dist = board.get_shortest_path_len(opp_player.pos, opp_player.goal_row)
        if ai_dist == 0: return 1000
        if opp_dist == 0: return -1000

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
                self.apply_move(sim_board, sim_opp, sim_ai, move) # Opponent is moving
                
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
            
        # 2. Wall Moves (Only check if player has walls)
        if active_player.walls_remaining > 0:
            # We search a 2-cell radius around both players.
            # This allows the AI to place walls slightly further away to create bottlenecks.
            focus_points = [active_player.pos, waiting_player.pos]
            checked_spots = set()
            
            for fx, fy in focus_points:
                for cx in range(fx - 2, fx + 2):
                    for cy in range(fy - 2, fy + 2):
                        if 0 <= cx < BOARD_SIZE - 1 and 0 <= cy < BOARD_SIZE - 1:
                            if (cx, cy) in checked_spots: continue
                            checked_spots.add((cx, cy))
                            
                            # Test Horizontal
                            test_h = board.clone()
                            if test_h.place_wall(cx, cy, 'H', active_player, waiting_player):
                                moves.append(('wall', (cx, cy), 'H'))
                            
                            # Test Vertical
                            test_v = board.clone()
                            if test_v.place_wall(cx, cy, 'V', active_player, waiting_player):
                                moves.append(('wall', (cx, cy), 'V'))
        return moves

    def apply_move(self, board, active_player, waiting_player, move):
        m_type = move[0]
        if m_type == 'move':
            active_player.pos = move[1]
        elif m_type == 'wall':
            coords = move[1]
            orient = move[2]
            board.place_wall(coords[0], coords[1], orient, active_player, waiting_player)
            active_player.walls_remaining -= 1

    def clone_player(self, player):
        from player import Player
        p = Player(player.pos, player.color, player.goal_row, player.id)
        p.walls_remaining = player.walls_remaining
        return p