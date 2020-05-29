import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { tap } from 'rxjs/operators';

@Injectable({
	providedIn: 'root'
})
export class SocketService {

	myWebSocket: WebSocketSubject<object>;

	constructor() { }

	go() {
		console.log('go called');
		this.myWebSocket = webSocket('ws://192.168.1.109:8765');

		console.log(this.myWebSocket);
		this.myWebSocket.subscribe(dataFromServer => console.log('direct : ' + dataFromServer));

		this.myWebSocket.pipe(
			tap(a => console.log('a'))
		);

		this.myWebSocket.asObservable().subscribe(dataFromServer => console.log(dataFromServer));
		this.myWebSocket.next({message: 'gotcha fam'});

		setInterval(this.asdf, 1000, this.myWebSocket);
	}

	asdf(myWebSocket: WebSocketSubject<object>) {
		console.log(myWebSocket);
		myWebSocket.next({message: 'gotcha fam2'});
	}
}
