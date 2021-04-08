class ModelHandler:

    def update_status(self, status):
        self.status = status
        self.save()
