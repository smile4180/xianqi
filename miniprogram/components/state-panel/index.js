Component({
  properties: { state: { type: String, value: 'idle' }, message: String },
  methods: { retry() { this.triggerEvent('retry'); } },
});
