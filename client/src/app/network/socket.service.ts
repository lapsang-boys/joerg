import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Observable, Subject } from 'rxjs';
import { FromJson } from './from.json';

@Injectable({
	providedIn: 'root'
})
export class SocketService {
	private socket: WebSocketSubject<object>;
	private typeSubject: Map<string, Subject<object>> = new Map();


	constructor() { }

	go() {
		console.log('go called');
		this.socket = webSocket('ws://192.168.1.109:8000');
		console.log(this.socket);
		this.socket.asObservable().subscribe(data => this.routeServerData(data));
		this.socket.next({type: 'new_game'});
	}

	private routeServerData(dataFromServer: object) {
		const subject = this.typeSubject.get(dataFromServer['type']);
		if (!subject) {
			console.warn('no subscriber for:', dataFromServer);
			return;
		}
		subject.next(dataFromServer);
	}

	getTypeObservable<T extends FromJson>(type: string): Observable<object> {
		if (this.typeSubject.has(type)) {
			return this.typeSubject.get(type).asObservable();
		}
		const typeSubject = new Subject<T>()
		this.typeSubject.set(type, typeSubject);
		return this.typeSubject.get(type).asObservable();
	}
}
