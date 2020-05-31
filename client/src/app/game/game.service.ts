import { Injectable } from '@angular/core';
import { SocketService } from '../network/socket.service';
import { Observable, Subject } from 'rxjs';
import { Board } from './types/board.type';

@Injectable({
	providedIn: 'root'
})
export class GameService {
	private boardSubject: Subject<Board> = new Subject();
	private board: Board;

	constructor(private socket: SocketService) { }

	start() {
		this.socket.go();
		this.socket.getTypeObservable<Board>('board').subscribe(payload => this.handleUpdate(payload));
	}

	next() {
		this.socket.send({type: 'next_action', board_id: this.board.board_id})
	}

	handleUpdate(payload: object) {
		const rawBoard = payload['board'];
		const boardId = payload['board_id']
		this.board = new Board(boardId);
		this.board.fromJson(rawBoard);
		this.boardSubject.next(this.board);
	}

	getObservableBoard(): Observable<Board> {
		return this.boardSubject.asObservable();
	}
}
