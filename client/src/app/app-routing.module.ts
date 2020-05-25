import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LibraryOverviewComponent } from './library/library-overview/library-overview.component';
import { HomeComponent } from './splashscreen/home/home.component';


const routes: Routes = [
	{
		path: '',
		component: HomeComponent
	},
	{
		path: 'library',
		component: LibraryOverviewComponent
	},
	{ path: '**', redirectTo: '' }
];

@NgModule({
	imports: [RouterModule.forRoot(routes)],
	exports: [RouterModule]
})
export class AppRoutingModule { }
