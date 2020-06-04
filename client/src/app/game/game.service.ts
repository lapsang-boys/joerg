import { Injectable } from '@angular/core';
import { SocketService } from '../network/socket.service';
import { Observable, Subject } from 'rxjs';
import { Board } from './types/board.type';
import { Choice } from './types/choice.type';
import { JoergError } from './types/joerg-error.type';

@Injectable({
	providedIn: 'root'
})
export class GameService {
	private boardSubject: Subject<Board> = new Subject();
	private choiceSubject: Subject<Choice> = new Subject();
	private errorSubject: Subject<JoergError> = new Subject();
	private board: Board;

	constructor(private socket: SocketService) { }

	start() {
		this.socket.go();
		this.socket.getTypeObservable<Board>('board').subscribe(payload => this.boardUpdate(payload));
		this.socket.getTypeObservable<Choice>('choice').subscribe(payload => this.choiceUpdate(payload));
		this.socket.getTypeObservable<JoergError>('error').subscribe(payload => this.errorUpdate(payload));
	}

	next() {
		this.socket.send({type: 'nextAction', boardId: this.board.boardId})
	}

	boardUpdate(payload: object) {
		const rawBoard = payload['board'];
		const boardId = payload['boardId']
		this.board = new Board(boardId);
		this.board.fromJson(rawBoard);
		this.boardSubject.next(this.board);
	}

	choiceUpdate(payload: object) {
		const rawChoice = payload;
		const choice = new Choice();
		choice.fromJson(rawChoice);
		this.choiceSubject.next(choice);
	}

	errorUpdate(payload: object) {
		const joergError = new JoergError();
		joergError.fromJson(payload["error"]);
		this.errorSubject.next(joergError);
	}

	getObservableBoard(): Observable<Board> {
		return this.boardSubject.asObservable();
	}

	getObservableChoice(): Observable<Choice> {
		return this.choiceSubject.asObservable();
	}

	makeChoice(choiceIndex: number): void {
		this.socket.send({type: "choice", "choice": choiceIndex})
	}
}
