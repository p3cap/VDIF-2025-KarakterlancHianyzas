using Godot;
using System;

public partial class Data : Node
{
	[Signal]
	public delegate void UpdateOutcomeEventHandler(); // EmitSignal("UpdateOutcome"); Connect("UpdateOutcome", this, nameof(OnSignalThree));
	public int round;
	
	public override void _Ready(){
		round = 0;
		
	}
}
