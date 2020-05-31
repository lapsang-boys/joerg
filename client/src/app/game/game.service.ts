import { Injectable } from '@angular/core';
import { SocketService } from '../network/socket.service';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { Board } from './types/board.type';

@Injectable({
	providedIn: 'root'
})
export class GameService {
	private boardSubject: Subject<Board> = new Subject();

	constructor(private socket: SocketService) { }

	start() {
		this.socket.go();
		this.socket.getTypeObservable<Board>('board').subscribe(payload => this.handleUpdate(payload['board']));
	}

	handleUpdate(rawBoard: object) {
		console.log(rawBoard);
		const b = new Board();
		b.fromJson(rawBoard);
		this.boardSubject.next(b);
	}

	getObservableBoard(): Observable<Board> {
		return this.boardSubject.asObservable();
	}
}
