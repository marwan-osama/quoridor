# ai.py
import random
from settings import *

class AI:
    def __init__(self, player_id):
        self.id = player_id

    def get_best_move(self, board, p1, p2):
        """Root of the Minimax algorithm."""
        # p1 is Human (Maximizer for heuristic perspective? No, usually AI maximizes its own score)
        # Let's say: AI is Maximizer.
        # AI wants to Minimize its distance and Maximize P1's distance.
        # Score = P1_Dist - AI_Dist.
        
        # We need to clone players to not affect real game during recursion
        # But players are simple objects, we can just create copies or update temp ones.
        # Actually, simpler to pass player state data.
        
        print("AI Thinking...")
        best_score = -float('inf')
        best_move = None
        
        # Determine who is the AI player object
        ai_player = p2 if self.id == 2 else p1
        opp_player = p1 if self.id == 2 else p2

        possible_moves = self.get_all_moves(board, ai_player, opp_player)
        
        alpha = -float('inf')
        beta = float('inf')

        for move in possible_moves:
            # Simulate
            sim_board = board.clone()
            sim_ai = self.clone_player(ai_player)
            sim_opp = self.clone_player(opp_player)
            
            self.apply_move(sim_board, sim_ai, sim_opp, move)
            
            score = self.minimax(sim_board, AI_DEPTH - 1, alpha, beta, False, sim_ai, sim_opp)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
            if beta <= alpha:
                break
                
        return best_move

    def minimax(self, board, depth, alpha, beta, is_maximizing, ai_player, opp_player):
        # 1. Base Case
        ai_dist = board.get_shortest_path_len(ai_player.pos, ai_player.goal_row)
        opp_dist = board.get_shortest_path_len(opp_player.pos, opp_player.goal_row)

        if ai_dist == 0: return INF # AI Won
        if opp_dist == 0: return -INF # Opponent Won
        if depth == 0:
            return opp_dist - ai_dist # Heuristic

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
            # Opponent moves
            moves = self.get_all_moves(board, opp_player, ai_player)
            for move in moves:
                sim_board = board.clone()
                sim_ai = self.clone_player(ai_player)
                sim_opp = self.clone_player(opp_player)
                # Apply move for opponent
                self.apply_move(sim_board, opp_player, ai_player, move) # Note: swap roles in apply helper
                
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
        # Optimization: Only check walls near players to reduce search space (heuristic pruning)
        if active_player.walls_remaining > 0:
            # Check a grid around the players
            focus_points = [active_player.pos, waiting_player.pos]
            checked = set()
            
            for fx, fy in focus_points:
                # Search range: 2 cells around players
                for cx in range(fx-2, fx+2):
                    for cy in range(fy-2, fy+2):
                        if 0 <= cx < BOARD_SIZE-1 and 0 <= cy < BOARD_SIZE-1:
                            if (cx, cy) in checked: continue
                            checked.add((cx, cy))
                            
                            # Try Horizontal
                            if board.place_wall(cx, cy, 'H', active_player, waiting_player):
                                # Must undo immediately as place_wall modifies board
                                # Actually place_wall checks validation, so we just want to know if it's legal
                                # We need to revert the board manually or clone just for checking.
                                # Since place_wall modifies the board, we can't use it directly in a generator 
                                # efficiently without reverting.
                                # STRATEGY: Use clone for check? Too slow.
                                # STRATEGY: Modify board.place_wall to have a 'check_only' flag or manual revert.
                                # For this project, let's assume we pass a clone to place_wall or use the clone method inside.
                                
                                # To keep it simple: Let's use a temp clone here. 
                                # It's slow but safe for a student project.
                                temp_board = board.clone()
                                if temp_board.place_wall(cx, cy, 'H', active_player, waiting_player):
                                    moves.append(('wall', (cx, cy), 'H'))
                                
                                temp_board = board.clone()
                                if temp_board.place_wall(cx, cy, 'V', active_player, waiting_player):
                                    moves.append(('wall', (cx, cy), 'V'))
                                    
        # Shuffle to add randomness if scores are equal
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
        from player import Player # Local import to avoid circular dependency
        p = Player(player.pos, player.color, player.goal_row, player.id)
        p.walls_remaining = player.walls_remaining
        return p